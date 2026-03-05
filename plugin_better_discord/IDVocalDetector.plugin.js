/**
 * @name VocalChangeAlert
 * @version 1.4.0
 * @description Alerte au changement de vocal et envoie via WebSocket au serveur backend. Envoie "none" si déconnecté.
 */

module.exports = class VocalChangeAlert {
    constructor() {
        this.name = "VocalChangeAlert";
        this.version = "1.4.0";
        this.description = "Alerte au changement de vocal et envoi WS";
        this.interval = null;
        this.lastVocal = null;
        this.ws = null;
        this.wsConnected = false;
        this.reconnectTimeout = null;
    }

    start() {
        console.log("%c[VocalChangeAlert] Plugin démarré", "color: #43b581;");
        this.connectWS();

        this.interval = setInterval(() => {
            const { guildId, vocalId } = this.getCurrentVocal();

            if (vocalId !== this.lastVocal) {
                this.lastVocal = vocalId;
                console.log("[VocalChangeAlert] Changement détecté :", { guildId, vocalId });
                this.sendWS({ guildId, vocalId, type: "update" });
            }
        }, 1000);
    }

    stop() {
        console.log("%c[VocalChangeAlert] Plugin arrêté", "color: #f04747;");
        if (this.interval) clearInterval(this.interval);
        if (this.ws) this.ws.close();
        if (this.reconnectTimeout) clearTimeout(this.reconnectTimeout);
    }

    // ================================
    // Détection vocal actuelle
    // ================================

    getCurrentVocal() {
        const filtered = Array.from(document.getElementsByTagName('div')).filter(div =>
            Array.from(div.classList).some(cls => cls.startsWith("lineClamp1__")) &&
            div.getAttribute("data-text-variant") === "text-xs/medium" &&
            div.baseURI.startsWith("https://discord.com/channels/")
        );

        let guildId = null;
        let vocalId = null;

        if (filtered[0]) {
            try {
                const urlParts = filtered[0].parentNode.parentNode.href
                    .split('channels/')[1]
                    .split('/');

                guildId = urlParts[0];
                vocalId = urlParts[1];
            } catch (e) {
                console.warn("[VocalChangeAlert] Erreur parsing URL :", e);
            }
        }

        if (!vocalId) vocalId = "none";

        return { guildId, vocalId };
    }

    // ================================
    // WebSocket
    // ================================

    connectWS() {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) return;

        this.ws = new WebSocket("ws://127.0.0.1:8888/ws");

        this.ws.onopen = () => {
            console.log("[VocalChangeAlert] WS connecté");
            this.wsConnected = true;

            // 🔥 Envoi immédiat de l’état actuel
            const { guildId, vocalId } = this.getCurrentVocal();
            this.lastVocal = vocalId;

            this.sendWS({ guildId, vocalId, type: "init" });
        };

        this.ws.onmessage = (event) => {
            console.log("[VocalChangeAlert] Réponse serveur :", event.data);
        };

        this.ws.onerror = (err) => {
            console.error("[VocalChangeAlert] Erreur WS :", err);
        };

        this.ws.onclose = () => {
            console.log("[VocalChangeAlert] WS fermé, tentative de reconnexion dans 1s...");
            this.wsConnected = false;

            this.reconnectTimeout = setTimeout(() => {
                this.connectWS();
            }, 1000);
        };
    }

    sendWS(payload) {
        if (this.wsConnected && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(payload));
        } else {
            console.warn("[VocalChangeAlert] WS pas prête, message ignoré");
        }
    }
};