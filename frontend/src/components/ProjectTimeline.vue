<template>
  <div class="soc-timeline-wrapper" ref="wrapperEl">

    <!-- ══════════════════════════════════════════════
         HEADER — Titre hero du projet mémoire
    ════════════════════════════════════════════════ -->
    <div class="soc-hero-header">
      <span class="soc-hero-badge">
        <ShieldCheck :size="14" />
        Réalisation à la une
      </span>
      <h2 class="soc-hero-title">
        SOC Open-Source :<br />
        <span class="soc-hero-title--accent">Incident Response Evolution</span>
      </h2>
      <p class="soc-hero-desc">
        Conception, déploiement et validation d'un Centre d'Opérations de Sécurité (SOC) complet
        pour l'entreprise <strong>PANESS IT</strong>, fondé exclusivement sur des technologies open‑source et
        validé par 4 scénarios d'attaque réels. Mémoire de fin de cycle — Samnick Biga Raoul Aubin (IHTM).
      </p>
      <div class="soc-hero-pills">
        <span class="soc-pill pill--orange">Wazuh v4.14.5</span>
        <span class="soc-pill pill--red">Suricata NIDS</span>
        <span class="soc-pill pill--purple">YARA v4.5.1</span>
        <span class="soc-pill pill--blue">DeepSeek AI</span>
        <span class="soc-pill pill--indigo">MISP &amp; DFIR‑IRIS</span>
        <span class="soc-pill pill--green">Shuffle SOAR</span>
        <span class="soc-pill pill--teal">Telegram Bot</span>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════
         TERMINAL BAR — Ligne commande défilante
    ════════════════════════════════════════════════ -->
    <div class="soc-terminal-bar" aria-hidden="true">
      <span class="term-prompt">root@soc-lab:~#</span>
      <span class="term-cmd" ref="termCmdEl">incident_response --timeline --verbose --phases=9</span>
      <span class="term-cursor">▋</span>
    </div>

    <!-- ══════════════════════════════════════════════
         TIMELINE VERTICALE CENTRÉE
    ════════════════════════════════════════════════ -->
    <div class="soc-timeline-track" role="list">
      <!-- Ligne verticale centrale -->
      <div class="soc-center-line" aria-hidden="true">
        <div class="soc-center-line__fill" :style="{ height: lineProgress + '%' }"></div>
      </div>

      <!-- ITEMS ALTERNANT GAUCHE / DROITE -->
      <div
        v-for="(phase, idx) in phases"
        :key="phase.id"
        class="soc-phase-row"
        :class="[
          idx % 2 === 0 ? 'phase-row--left' : 'phase-row--right',
          { 'phase-row--visible': visiblePhases.has(idx) },
          `phase-row--${phase.severity}`,
        ]"
        :data-phase-idx="idx"
        role="listitem"
      >
        <!-- Côté vide (espace) -->
        <div class="soc-phase-side soc-phase-side--empty" aria-hidden="true"></div>

        <!-- Marqueur central cliquable -->
        <div class="soc-phase-center">
          <button
            class="soc-phase-marker"
            :class="`soc-phase-marker--${phase.severity}`"
            type="button"
            :aria-label="`Voir les détails de la phase ${phase.number} : ${phase.title}`"
            @click="openModal(phase)"
          >
            <component :is="phase.icon" :size="18" />
          </button>
          <span class="soc-phase-number">{{ String(idx + 1).padStart(2, '0') }}</span>
        </div>

        <!-- Carte du contenu -->
        <div class="soc-phase-side soc-phase-side--content">
          <article class="soc-phase-card glass-card">
            <!-- Badge criticité + Tool tag -->
            <div class="soc-phase-card__meta">
              <span class="severity-badge" :class="`severity-badge--${phase.severity}`">
                <component :is="severityIcon(phase.severity)" :size="11" />
                {{ severityLabel(phase.severity) }}
              </span>
              <span class="tool-tag" v-if="phase.tool">{{ phase.tool }}</span>
            </div>

            <h3 class="soc-phase-card__title">{{ phase.title }}</h3>
            <p class="soc-phase-card__body">{{ phase.body }}</p>

            <!-- Terminal output box -->
            <div v-if="phase.snippet" class="soc-term-box">
              <div class="soc-term-box__bar" aria-hidden="true">
                <span class="dot dot--red"></span>
                <span class="dot dot--yellow"></span>
                <span class="dot dot--green"></span>
                <span class="soc-term-box__label">{{ phase.snippetLabel || 'console output' }}</span>
              </div>
              <pre class="soc-term-box__code"><code>{{ phase.snippet }}</code></pre>
            </div>

            <!-- Bouton modal logs / playbooks -->
            <button class="soc-detail-btn" type="button" @click="openModal(phase)">
              <FileText :size="13" />
              Voir les logs et playbooks
            </button>
          </article>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════
         BANDE RÉSULTATS — Métriques du mémoire
    ════════════════════════════════════════════════ -->
    <div class="soc-results-band">
      <div v-for="kpi in kpis" :key="kpi.label" class="soc-kpi">
        <span class="soc-kpi__value">{{ kpi.value }}</span>
        <span class="soc-kpi__label">{{ kpi.label }}</span>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════
         BOUTON PDF — Consultation mémoire
    ════════════════════════════════════════════════ -->
    <div class="soc-footer-cta" v-if="pdfUrl">
      <a :href="pdfUrl" target="_blank" rel="noreferrer" class="button primary soc-pdf-btn">
        <FileText :size="17" />
        Consulter le mémoire complet (PDF)
      </a>
    </div>

    <!-- ══════════════════════════════════════════════
         MODALE DÉTAIL — Logs / Playbooks / Règles
    ════════════════════════════════════════════════ -->
    <Teleport to="body">
      <Transition name="soc-modal-fade">
        <div
          v-if="activePhase"
          class="soc-modal-backdrop"
          role="presentation"
          @click.self="closeModal"
        >
          <div class="soc-modal glass-card" role="dialog" aria-modal="true" :aria-labelledby="`modal-title-${activePhase.id}`">
            <div class="soc-modal__header">
              <div>
                <span class="severity-badge" :class="`severity-badge--${activePhase.severity}`">
                  <component :is="severityIcon(activePhase.severity)" :size="12" />
                  {{ severityLabel(activePhase.severity) }}
                </span>
                <span class="soc-modal__tool" v-if="activePhase.tool">{{ activePhase.tool }}</span>
              </div>
              <button class="soc-modal__close" type="button" @click="closeModal" aria-label="Fermer">
                <X :size="20" />
              </button>
            </div>

            <h3 :id="`modal-title-${activePhase.id}`" class="soc-modal__title">{{ activePhase.title }}</h3>
            <p class="soc-modal__desc">{{ activePhase.body }}</p>

            <!-- Logs / Règles / Playbook dans terminal -->
            <div class="soc-term-box">
              <div class="soc-term-box__bar" aria-hidden="true">
                <span class="dot dot--red"></span>
                <span class="dot dot--yellow"></span>
                <span class="dot dot--green"></span>
                <span class="soc-term-box__label">{{ activePhase.modalLabel || 'logs / playbook / règles' }}</span>
              </div>
              <pre class="soc-term-box__code soc-term-box__code--modal"><code>{{ activePhase.playbook }}</code></pre>
            </div>

            <!-- Détails technique supplémentaires -->
            <div v-if="activePhase.details?.length" class="soc-modal__details">
              <h4>Points techniques clés</h4>
              <ul>
                <li v-for="d in activePhase.details" :key="d">{{ d }}</li>
              </ul>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import {
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  Info,
  Server,
  Radio,
  Cpu,
  Zap,
  Send,
  Database,
  Terminal,
  FileText,
  CheckCircle,
  X,
  Bug,
  Network,
  HardDrive,
} from 'lucide-vue-next';

defineProps({
  pdfUrl: { type: String, default: '' },
});

const wrapperEl = ref(null);
const termCmdEl = ref(null);
const activePhase = ref(null);
const visiblePhases = ref(new Set());
const lineProgress = ref(0);

// ──────────────────────────────────────────────
// KPIs du mémoire
// ──────────────────────────────────────────────
const kpis = [
  { value: '9', label: 'Phases de déploiement' },
  { value: '5', label: 'VMs VirtualBox NAT' },
  { value: '4', label: 'Scénarios d\'attaque validés' },
  { value: '< 3s', label: 'Temps de réponse aux incidents' },
  { value: '0 €', label: 'Coût licences logicielles' },
  { value: '7', label: 'Outils SOC intégrés' },
];

// ──────────────────────────────────────────────
// Helpers sévérité
// ──────────────────────────────────────────────
function severityLabel(s) {
  return { critical: 'CRITICAL', high: 'HIGH', medium: 'MEDIUM', info: 'INFO' }[s] || 'INFO';
}
function severityIcon(s) {
  return { critical: ShieldAlert, high: AlertTriangle, medium: Info, info: Info }[s] || Info;
}

// ──────────────────────────────────────────────
// PHASES DU MÉMOIRE (ordre chronologique exact)
// ──────────────────────────────────────────────
const phases = [
  {
    id: 'contexte',
    title: 'Contexte & Présentation du Projet',
    tool: 'PANESS IT',
    icon: Info,
    severity: 'info',
    snippetLabel: 'objectif du mémoire',
    body: 'Architecture complète d\'un centre d\'opérations de sécurité (SOC) fondé exclusivement sur des outils open‑source, conçue, déployée et validée en environnement virtualisé pour l\'entreprise PANESS IT (PME informatique de Yaoundé). Mémoire de Licence Professionnelle RSI — IHTM.',
    snippet: `Architecture SOC Open-Source — PANESS IT (2026)
Infrastructure : VirtualBox NAT 192.168.100.0/24
Auteur        : Samnick Biga Raoul Aubin
Encadreur pro : M. Awouafack Fabien (PANESS)
Encadreur acad: M. Teka Wilfried (IHTM)
Objectif      : SOC/SIEM/EDR complet 0€ de licences`,
    playbook: `# Architecture VirtualBox NAT — 5 Machines Virtuelles
wazuh-server  : Amazon Linux 2023 (OVA)  — 192.168.100.10
soc-services  : Ubuntu 24.04 (Docker)    — 192.168.100.20
agent-linux   : Debian 12               — 192.168.100.30
agent-windows : Windows 10 Pro          — 192.168.100.40
kali-attacker : Kali Linux              — 192.168.100.50

Réseau NAT dédié: SOC-Network (192.168.100.0/24)
Hyperviseur: Oracle VirtualBox 7.0`,
    modalLabel: 'Architecture du laboratoire',
    details: [
      'Réseau NAT isolé VirtualBox (SOC-Network) simulant un environnement d\'entreprise réel',
      'Conformité MITRE ATT&CK pour la cartographie des attaques testées',
      'Approche défensive bleue (Blue Team) avec simulation rouge (Red Team) via Kali Linux',
      'Stack entièrement open-source : Wazuh, Suricata, MISP, IRIS, Shuffle, YARA, DeepSeek',
    ],
  },
  {
    id: 'infra-wazuh',
    title: 'Phase 1 — Installation Infrastructure Wazuh',
    tool: 'Wazuh v4.14.5',
    icon: Server,
    severity: 'info',
    snippetLabel: '/var/ossec/etc/ossec.conf',
    body: 'Déploiement du serveur Wazuh (SIEM central) via l\'OVA officielle sur Amazon Linux 2023. Configuration du Manager avec OpenSearch intégré, du Wazuh Dashboard (:443) et paramétrage des seuils d\'alertes. Point d\'entrée unique pour la corrélation de tous les événements de sécurité.',
    snippet: `[root@wazuh-server ~]# systemctl status wazuh-manager
● wazuh-manager.service — Wazuh Manager
   Loaded: loaded (/lib/systemd/system/wazuh-manager.service)
   Active: active (running) since 2026-06-10T08:00:00
[INFO] Wazuh Manager v4.14.5 — Running
[INFO] OpenSearch Dashboard accessible sur :443`,
    playbook: `# Configuration ossec.conf (extrait)
<ossec_config>
  <global>
    <jsonout_output>yes</jsonout_output>
    <alerts_log>yes</alerts_log>
    <logall>no</logall>
    <email_notification>no</email_notification>
    <smtp_server>localhost</smtp_server>
    <email_from>wazuh@paness.local</email_from>
  </global>
  <alerts>
    <log_alert_level>3</log_alert_level>
    <email_alert_level>12</email_alert_level>
  </alerts>
  <remote>
    <connection>secure</connection>
    <port>1514</port>
    <protocol>tcp</protocol>
  </remote>
</ossec_config>`,
    modalLabel: 'ossec.conf — Configuration Wazuh Manager',
    details: [
      'OVA Wazuh 4.14.5 importée sur VirtualBox — Amazon Linux 2023 préconfigurée',
      'OpenSearch Dashboard accessible via HTTPS (:443) pour la visualisation des alertes',
      'Port 1514 (TCP) pour la communication sécurisée Agents ↔ Manager',
      'Seuil d\'alerte email configuré à niveau 12 pour les incidents critiques',
    ],
  },
  {
    id: 'agents',
    title: 'Phase 2 — Déploiement des Agents Wazuh',
    tool: 'Wazuh Agent',
    icon: HardDrive,
    severity: 'info',
    snippetLabel: 'agent enrollment output',
    body: 'Installation et enregistrement des agents Wazuh sur les endpoints (Debian 12 et Windows 10 Pro). Configuration du canal chiffré entre chaque agent et le Manager central. Vérification de la remontée des logs système, sécurité et applications en temps réel vers le SIEM.',
    snippet: `[agent-linux] Wazuh Agent enrollment...
[INFO] Agent ID: 001 — Name: agent-linux
[INFO] Connected to Manager 192.168.100.10:1514
[OK] Logs syslog, auth.log — actifs

[agent-windows] Agent enrollment...
[INFO] Agent ID: 002 — Name: agent-windows
[INFO] Windows Event Channel collecté
[OK] Security, System, Application — actifs`,
    playbook: `# Enregistrement agent Linux (Debian 12)
# 1. Installation
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --dearmor | sudo tee /usr/share/keyrings/wazuh.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list
sudo apt-get install wazuh-agent

# 2. Configuration
WAZUH_MANAGER="192.168.100.10" WAZUH_AGENT_NAME="agent-linux" dpkg -i wazuh-agent_4.14.5-1_amd64.deb

# 3. Activation
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent`,
    modalLabel: 'agent enrollment — ossec-authd',
    details: [
      'Agent Wazuh installé sur Debian 12 (agent-linux) et Windows 10 Pro (agent-windows)',
      'Canal chiffré TLS entre agents et Manager via port 1514 TCP',
      'Collecte automatique : auth.log, syslog, Windows Security Event Log',
      'Agent ID assigné automatiquement par le Manager lors de l\'enrollment',
    ],
  },
  {
    id: 'suricata',
    title: 'Phase 3 — Intégration Suricata NIDS',
    tool: 'Suricata 7.x',
    icon: Radio,
    severity: 'high',
    snippetLabel: '/var/log/suricata/eve.json',
    body: 'Déploiement de Suricata en mode NIDS (Network Intrusion Detection System) sur l\'interface eth2 du wazuh-server pour surveiller le trafic réseau de tout le sous-réseau SOC-Network. Téléchargement et activation des règles Emerging Threats Open. Intégration avec Wazuh via Filebeat pour la corrélation des alertes réseau.',
    snippet: `[ALERT] ET SCAN Potential SSH Scan OUTBOUND
Src IP: 192.168.100.50 (kali-attacker)
Dst IP: 192.168.100.30:22 (agent-linux)
Signature: 2001219 — Nmap SYN Scan Detection
[WAZUH] Rule 86601 triggered — Level 8`,
    playbook: `# Configuration suricata.yaml (extrait)
vars:
  address-groups:
    HOME_NET: "[192.168.100.0/24]"
    EXTERNAL_NET: "!$HOME_NET"

af-packet:
  - interface: eth2
    cluster-id: 99
    cluster-type: cluster_flow
    defrag: yes

rule-files:
  - /var/lib/suricata/rules/suricata.rules

outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      types: [alert, dns, http, tls]`,
    modalLabel: 'suricata.yaml + Emerging Threats rules',
    details: [
      'Suricata déployé en mode NIDS sur eth2 (interface interne SOC-Network)',
      'Règles Emerging Threats Open (ET/Open) mises à jour automatiquement via suricata-update',
      'Journal eve.json lu par l\'agent Wazuh via Filebeat → corrélation SIEM',
      'Détection : scans Nmap, attaques SSH, exfiltration DNS, anomalies TCP/UDP',
    ],
  },
  {
    id: 'fim-auditd',
    title: 'Phase 4 — FIM, Auditd & Sysmon (Surveillance Endpoints)',
    tool: 'FIM / Auditd / Sysmon',
    icon: Terminal,
    severity: 'critical',
    snippetLabel: 'Auditd + CDB suspicious-programs',
    body: 'File Integrity Monitoring (FIM) Wazuh surveillant les répertoires critiques (/home, /etc, /tmp) en temps réel. Auditd sous Linux (syscall execve) et Sysmon sous Windows (EventID 1) journalisant les exécutions de processus. Comparaison instantanée avec la liste CDB suspicious-programs pour bloquer les binaires dangereux.',
    snippet: `[AUDITD] execve() syscall captured:
comm="nc" (netcat) — pid=4823
[CDB] Match 'nc:red' in suspicious-programs
[RULE 100210] ALERT Level 12 fired !
  Desc: Commande suspecte détectée (nc)
  MITRE: T1059 — Command & Scripting Interpreter`,
    playbook: `<!-- local_rules.xml — Règle personnalisée CDB -->
<group name="auditd,sysmon,custom,">

  <!-- Règle 100210 : Commande suspecte via CDB -->
  <rule id="100210" level="12">
    <if_sid>80700</if_sid>
    <list field="audit.command" lookup="match_key">
      etc/lists/suspicious-programs
    </list>
    <description>
      Auditd: Commande suspecte via CDB: $(audit.command)
    </description>
    <mitre>
      <id>T1059</id>
    </mitre>
    <group>gdpr_IV_35.7.d,pci_dss_10.6.1,</group>
  </rule>

</group>

# Liste CDB /var/ossec/etc/lists/suspicious-programs
nc:red
ncat:red
netcat:red
nmap:red
tcpdump:yellow
wireshark:yellow`,
    modalLabel: 'local_rules.xml + CDB suspicious-programs',
    details: [
      'FIM Wazuh surveille /home, /etc/passwd, /etc/shadow, /tmp — modifications en temps réel',
      'Auditd capture les syscalls execve() sur agent-linux avec décodeur personnalisé',
      'Sysmon EventID 1 (Process Create) collecté sur agent-windows via Windows Event Channel',
      'Liste CDB suspicious-programs : nc, ncat, netcat, nmap, tcpdump, etc.',
    ],
  },
  {
    id: 'yara-fim',
    title: 'Phase 5 — YARA Active Response (Anti-Malware)',
    tool: 'YARA v4.5.1 + Valhalla',
    icon: Bug,
    severity: 'critical',
    snippetLabel: '/var/ossec/logs/active-responses.log',
    body: 'Déploiement de YARA v4.5.1 avec les règles Valhalla en Active Response Wazuh. Lors de toute modification détectée par FIM, le script yara.sh est déclenché automatiquement pour scanner le fichier créé. En cas de correspondance (ex. fichier EICAR), le script remove-threat.sh supprime le fichier malveillant en moins de 3 secondes.',
    snippet: `[FIM] New file detected: /home/raoulbiga/eicar_final6.txt
[AR] Triggering yara.sh on /home/raoulbiga/eicar_final6.txt
[YARA] Scanning with Valhalla rules...
[MATCH] EICAR_TEST_FILE — Signature: eicar_test
[INFO] Malware successfully deleted by remove-threat.sh
[WAZUH] Rule 108001 — Level 15 — YARA Alert fired`,
    playbook: `#!/bin/bash
# /var/ossec/active-response/bin/yara.sh (extrait)
YARA_PATH="/usr/local/bin/yara"
YARA_RULES="/var/ossec/active-response/yara/rules/yara_rules.yar"
FILENAME=$(echo $1 | cut -d'|' -f9)

# Scan YARA
YARA_OUTPUT=$("$YARA_PATH" -w -r -m "$YARA_RULES" "$FILENAME")

if [ -n "$YARA_OUTPUT" ]; then
  LOG="/var/ossec/logs/active-responses.log"
  echo "wazuh-YARA: INFO - Match: $YARA_OUTPUT" >> $LOG
  /var/ossec/active-response/bin/remove-threat.sh "$FILENAME"
fi

# Règle Wazuh (local_rules.xml)
# <rule id="108001" level="15">
#   <field name="yara_rule">.*</field>
#   <description>YARA: Malware détecté — $(yara_rule)</description>
# </rule>`,
    modalLabel: 'yara.sh + remove-threat.sh + règle 108001',
    details: [
      'YARA v4.5.1 compilé manuellement sur agent-linux et agent-windows (yara64.exe)',
      'Règles Valhalla couvrant plus de 20 000 signatures de malwares actifs',
      'Temps de réponse mesuré : < 3 secondes (FIM détection → suppression automatique)',
      'Test de validation : fichier EICAR (eicar_final6.txt) — détecté et supprimé avec succès',
    ],
  },
  {
    id: 'misp',
    title: 'Phase 6 — MISP Threat Intelligence',
    tool: 'MISP :1443',
    icon: Database,
    severity: 'high',
    snippetLabel: 'custom-misp.py — IOC correlation',
    body: 'Déploiement de MISP (Malware Information Sharing Platform) dans un conteneur Docker sur soc-services. Intégration via le script custom-misp.py qui interroge l\'API MISP pour corréler en temps réel les adresses IP suspectes détectées par Wazuh avec les flux de Threat Intelligence partagés.',
    snippet: `[WAZUH] Rule 5710: SSH Auth Failure x12
  Src IP: 192.168.100.50 (kali-attacker)
[MISP] custom-misp.py querying MISP API...
[MISP] GET /attributes/restSearch?value=192.168.100.50
[RESULT] IP flagged in malicious adversary campaign
[ALERT] IOC match confirmed — Escalating to IRIS`,
    playbook: `# /var/ossec/integrations/custom-misp.py (extrait)
import requests, json, sys

MISP_URL = "https://192.168.100.20:1443"
MISP_KEY  = "VOTRE-CLE-API-MISP"

def check_misp_ioc(ioc_value, ioc_type="ip-dst"):
    headers = {
        "Authorization": MISP_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "returnFormat": "json",
        "value": ioc_value,
        "type": ioc_type,
        "to_ids": 1
    }
    r = requests.post(
        f"{MISP_URL}/attributes/restSearch",
        headers=headers,
        json=payload,
        verify=False
    )
    attributes = r.json().get("response", {}).get("Attribute", [])
    return len(attributes) > 0`,
    modalLabel: 'custom-misp.py — MISP REST API',
    details: [
      'MISP déployé en Docker sur soc-services (:1443) avec base d\'IOCs pré-chargée',
      'Intégration native avec Wazuh via le répertoire /var/ossec/integrations/',
      'Corrélation automatique : IP suspectes brute-force SSH → vérification dans MISP',
      'Résultat : IP kali-attacker marquée dans un campaign d\'adversaire malveillant',
    ],
  },
  {
    id: 'deepseek',
    title: 'Phase 7 — Enrichissement IA avec DeepSeek',
    tool: 'DeepSeek AI API',
    icon: Cpu,
    severity: 'high',
    snippetLabel: 'custom-deepseek.py — LLM enrichissement',
    body: 'Intégration de l\'IA DeepSeek (LLM) pour enrichir automatiquement chaque alerte critique avec une explication en langage naturel : impact potentiel de la menace, contexte du vecteur d\'attaque et mesures de remédiation immédiates. Orchestré via le script custom-deepseek.py déclenché par Wazuh sur les alertes de niveau ≥ 10.',
    snippet: `[DEEPSEEK] Query: "Quel est l'impact de YARA rule: EICAR_TEST_FILE ?"
[RESPONSE] "Le fichier EICAR est un test standard simulant
une charge virale. Risque immédiat nul, mais sa présence
indique un test de sécurité ou une tentative d'intrusion.
Remédiation: Supprimer le fichier, vérifier l'origine."
[ENRICHMENT] Saved to alert context — Forwarded to IRIS`,
    playbook: `# /var/ossec/integrations/custom-deepseek.py (extrait)
import requests, json, sys

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_KEY = "sk-VOTRE-CLE-API"

def query_deepseek(description: str) -> str:
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{
            "role": "user",
            "content": (
                f"En un paragraphe concis, explique l'impact potentiel "
                f"et les mesures de remédiation pour cette menace: {description}"
            )
        }],
        "max_tokens": 300,
        "temperature": 0.3
    }
    r = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
    return r.json()["choices"][0]["message"]["content"]`,
    modalLabel: 'custom-deepseek.py — DeepSeek LLM API',
    details: [
      'API DeepSeek (deepseek-chat) utilisée pour l\'enrichissement contextuel des alertes',
      'Déclenchement automatique sur alertes Wazuh niveau ≥ 10 (High & Critical)',
      'Réponse en français : impact, vecteur d\'attaque, remédiation recommandée',
      'Résultat injecté dans le contexte de l\'alerte avant création du ticket IRIS',
    ],
  },
  {
    id: 'iris-telegram',
    title: 'Phase 8 — DFIR‑IRIS & Alerting Telegram',
    tool: 'DFIR-IRIS :8443 + Bot Telegram',
    icon: Send,
    severity: 'medium',
    snippetLabel: 'custom-wazuh_iris.py + custom-telegram.py',
    body: 'Création automatique de dossiers d\'incident structurés dans DFIR-IRIS via webhook lors de toute alerte critique. Simultanément, le bot Telegram envoie une notification instantanée formatée sur smartphone. Les analystes SOC sont alertés en temps réel sans avoir à consulter le dashboard Wazuh.',
    snippet: `[SOC PANESS] 🔴 Alerte CRITIQUE (Niveau 12)
Règle: 100210 — Commande suspecte (nc)
Agent: agent-linux (192.168.100.30)
Heure: 2026-06-29T14:42:53Z

[IRIS] Case #2 créé automatiquement
  Titre: "Commande suspecte nc sur agent-linux"
  Sévérité: Critical | Statut: Open`,
    playbook: `# custom-telegram.py (extrait)
import requests

BOT_TOKEN = "VOTRE-TOKEN-BOT"
CHAT_ID   = "VOTRE-CHAT-ID"

def format_alert(alert: dict) -> str:
    rule  = alert.get("rule", {})
    level = rule.get("level", 0)
    severity = "🔴 CRITIQUE" if level >= 12 else "🟠 ÉLEVÉ" if level >= 7 else "🟡 MOYEN"
    msg  = f"*[SOC PANESS]* {severity} (Niv.{level})\n"
    msg += f"Règle: {rule.get('id')} — {rule.get('description')}\n"
    msg += f"Agent: {alert.get('agent',{}).get('name')} ({alert.get('agent',{}).get('ip')})\n"
    msg += f"Heure: {alert.get('timestamp')}"
    return msg

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})`,
    modalLabel: 'custom-telegram.py + custom-wazuh_iris.py',
    details: [
      'DFIR-IRIS déployé en Docker sur soc-services (:8443) — SGBD PostgreSQL',
      'Tickets créés automatiquement avec titre, description, sévérité, horodatage et IOCs',
      'Bot Telegram Bot1 dédié au SOC PANESS — notification push instantanée',
      'Formatage Markdown Telegram : niveaux colorés, agent source, horodatage précis',
    ],
  },
  {
    id: 'shuffle',
    title: 'Phase 9 — Orchestration SOAR avec Shuffle',
    tool: 'Shuffle SOAR :3001',
    icon: Zap,
    severity: 'medium',
    snippetLabel: 'Shuffle Workflow — Automated Playbook',
    body: 'Déploiement de Shuffle SOAR pour orchestrer les flux de réponse automatisée. Les workflows Shuffle reçoivent les alertes Wazuh via webhook, interrogent VirusTotal pour la réputation des IOCs, appellent l\'API DeepSeek pour l\'enrichissement, créent le ticket IRIS et notifient Telegram — le tout de façon entièrement automatisée sans intervention humaine.',
    snippet: `[SHUFFLE] Webhook received — Wazuh Alert Level 15
[STEP 1] Extract IOCs from alert context
[STEP 2] VirusTotal API check: clean (0/70)
[STEP 3] DeepSeek enrichment: "Fichier EICAR..."
[STEP 4] IRIS Case creation: Case #3 — Open
[STEP 5] Telegram notification: sent ✓
[WORKFLOW] Completed in 4.2s — Status: SUCCESS`,
    playbook: `# Workflow Shuffle SOAR — Pipeline automatisé
# (Structure JSON simplifiée du workflow)

Trigger: Wazuh Webhook (HTTP POST :3001)
├── Action 1: Parse Alert JSON
│   └── Extract: alert.rule.id, alert.agent.ip
├── Action 2: VirusTotal Reputation Check
│   └── API: /api/v3/ip_addresses/{ip}
├── Action 3: DeepSeek LLM Enrichissement
│   └── Input: alert.rule.description
├── Action 4: DFIR-IRIS Create Case
│   └── POST /api/v1/cases — severity=critical
└── Action 5: Telegram Notification
    └── Bot1 — formatted Markdown message

# Configuration webhook Wazuh → Shuffle
<integration>
  <name>shuffle</name>
  <hook_url>http://192.168.100.20:3001/api/v1/hooks/HOOK_ID</hook_url>
  <level>9</level>
  <alert_format>json</alert_format>
</integration>`,
    modalLabel: 'Shuffle Workflow JSON + ossec.conf integration',
    details: [
      'Shuffle SOAR déployé en Docker sur soc-services (:3001) — OpenFlows compatible',
      'Workflow 5 étapes entièrement automatisé (0 intervention humaine)',
      'Intégrations natives : VirusTotal, DeepSeek, DFIR-IRIS, Telegram, Wazuh',
      'Temps d\'exécution moyen du workflow complet : 4,2 secondes',
    ],
  },
];

// ──────────────────────────────────────────────
// Scroll Reveal & Line Progress
// ──────────────────────────────────────────────
let observer;

function openModal(phase) {
  activePhase.value = phase;
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  activePhase.value = null;
  document.body.style.overflow = '';
}

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const idx = parseInt(entry.target.dataset.phaseIdx, 10);
          if (!isNaN(idx)) {
            setTimeout(() => {
              visiblePhases.value = new Set([...visiblePhases.value, idx]);
              // Avancer la ligne proportionnellement
              lineProgress.value = Math.round(((Math.max(...[...visiblePhases.value, idx]) + 1) / phases.length) * 100);
            }, idx * 80);
          }
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -80px 0px' },
  );

  document.querySelectorAll('.soc-phase-row').forEach((el) => observer.observe(el));

  // Animation typographie terminal
  if (termCmdEl.value) {
    const fullText = termCmdEl.value.textContent;
    termCmdEl.value.textContent = '';
    let i = 0;
    const type = () => {
      if (i < fullText.length) {
        termCmdEl.value.textContent += fullText[i++];
        setTimeout(type, 35 + Math.random() * 20);
      }
    };
    setTimeout(type, 400);
  }
});

onBeforeUnmount(() => {
  observer?.disconnect();
  document.body.style.overflow = '';
});
</script>

<style scoped>
/* ══════════════════════════════════════════════
   WRAPPER GLOBAL
══════════════════════════════════════════════ */
.soc-timeline-wrapper {
  width: 100%;
  padding: 0 0 40px;
  color: var(--text);
  font-family: 'Ubuntu', 'Ubuntu Sans', system-ui, sans-serif;
}

/* ══════════════════════════════════════════════
   HERO HEADER
══════════════════════════════════════════════ */
.soc-hero-header {
  max-width: 780px;
  margin: 0 auto 32px;
  text-align: center;
}

.soc-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #e95420;
  background: rgba(233, 84, 32, 0.08);
  border: 1px solid rgba(233, 84, 32, 0.22);
  padding: 5px 12px;
  border-radius: 20px;
  margin-bottom: 18px;
}

.soc-hero-title {
  margin: 0 0 14px;
  font-size: clamp(26px, 4vw, 38px);
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: #2c001e;
}

.soc-hero-title--accent {
  color: #e95420;
}

.soc-hero-desc {
  margin: 0 0 20px;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.7;
}

.soc-hero-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.soc-pill {
  font-size: 12px;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 14px;
  border: 1px solid transparent;
}

.pill--orange  { background: rgba(233,84,32,0.09);  color: #e95420; border-color: rgba(233,84,32,0.25); }
.pill--red     { background: rgba(220,38,38,0.08);  color: #dc2626; border-color: rgba(220,38,38,0.22); }
.pill--purple  { background: rgba(119,33,111,0.09); color: #77216f; border-color: rgba(119,33,111,0.22); }
.pill--blue    { background: rgba(37,99,235,0.08);  color: #1d4ed8; border-color: rgba(37,99,235,0.2); }
.pill--indigo  { background: rgba(67,56,202,0.08);  color: #4338ca; border-color: rgba(67,56,202,0.2); }
.pill--green   { background: rgba(5,150,105,0.08);  color: #059669; border-color: rgba(5,150,105,0.2); }
.pill--teal    { background: rgba(20,184,166,0.08); color: #0d9488; border-color: rgba(20,184,166,0.2); }

/* ══════════════════════════════════════════════
   BARRE TERMINAL
══════════════════════════════════════════════ */
.soc-terminal-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 680px;
  margin: 0 auto 56px;
  padding: 12px 18px;
  border-radius: 12px;
  background: rgba(8, 3, 14, 0.9);
  border: 1px solid rgba(233, 84, 32, 0.2);
  font-family: 'Ubuntu Mono', 'Fira Code', monospace;
  font-size: 13px;
  box-shadow: 0 8px 28px rgba(44, 0, 30, 0.14);
}

.term-prompt { color: #10b981; font-weight: 700; white-space: nowrap; }
.term-cmd    { color: rgba(255,255,255,0.82); flex: 1; }
.term-cursor { color: #e95420; animation: blink 0.9s step-end infinite; }

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

/* ══════════════════════════════════════════════
   TRACK TIMELINE CENTRÉ
══════════════════════════════════════════════ */
.soc-timeline-track {
  position: relative;
  max-width: 1100px;
  margin: 0 auto;
}

/* Ligne centrale */
.soc-center-line {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 3px;
  background: rgba(119, 33, 111, 0.12);
  border-radius: 3px;
  z-index: 1;
  overflow: hidden;
}

.soc-center-line__fill {
  width: 100%;
  background: linear-gradient(180deg, #e95420 0%, #77216f 55%, #c48abc 100%);
  border-radius: 3px;
  transition: height 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ══════════════════════════════════════════════
   LIGNE DE PHASE (3 colonnes : vide | centre | contenu)
══════════════════════════════════════════════ */
.soc-phase-row {
  display: grid;
  grid-template-columns: 1fr 64px 1fr;
  gap: 0;
  align-items: start;
  margin-bottom: 64px;
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.55s ease, transform 0.55s cubic-bezier(0.23, 1, 0.32, 1);
}

.soc-phase-row--visible {
  opacity: 1;
  transform: translateY(0);
}

/* Lignes paires : carte à gauche, vide à droite */
.soc-phase-row.phase-row--left .soc-phase-side--empty   { order: 3; }
.soc-phase-row.phase-row--left .soc-phase-center        { order: 2; }
.soc-phase-row.phase-row--left .soc-phase-side--content { order: 1; text-align: right; }
.soc-phase-row.phase-row--left .soc-phase-side--content { padding-right: 28px; }

/* Lignes impaires : vide à gauche, carte à droite */
.soc-phase-row.phase-row--right .soc-phase-side--empty   { order: 1; }
.soc-phase-row.phase-row--right .soc-phase-center        { order: 2; }
.soc-phase-row.phase-row--right .soc-phase-side--content { order: 3; padding-left: 28px; }

.soc-phase-side { width: 100%; }

/* Centre : marqueur + numéro */
.soc-phase-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 2;
  padding-top: 16px;
}

.soc-phase-number {
  font-family: 'Ubuntu Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: rgba(119, 33, 111, 0.5);
  letter-spacing: 0.05em;
}

/* Marqueur cliquable */
.soc-phase-marker {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  cursor: pointer;
  border: 2.5px solid;
  background: #fff;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s;
  flex-shrink: 0;
}

.soc-phase-marker:hover,
.soc-phase-marker:focus-visible {
  transform: scale(1.18);
  outline: none;
}

.soc-phase-marker--critical {
  border-color: #dc2626;
  color: #dc2626;
  box-shadow: 0 4px 16px rgba(220, 38, 38, 0.18);
}
.soc-phase-marker--critical:hover { box-shadow: 0 0 0 8px rgba(220, 38, 38, 0.14); }

.soc-phase-marker--high {
  border-color: #e95420;
  color: #e95420;
  box-shadow: 0 4px 16px rgba(233, 84, 32, 0.18);
}
.soc-phase-marker--high:hover { box-shadow: 0 0 0 8px rgba(233, 84, 32, 0.14); }

.soc-phase-marker--medium {
  border-color: #77216f;
  color: #77216f;
  box-shadow: 0 4px 14px rgba(119, 33, 111, 0.14);
}
.soc-phase-marker--medium:hover { box-shadow: 0 0 0 8px rgba(119, 33, 111, 0.12); }

.soc-phase-marker--info {
  border-color: #005a9c;
  color: #005a9c;
  box-shadow: 0 4px 14px rgba(0, 90, 156, 0.12);
}
.soc-phase-marker--info:hover { box-shadow: 0 0 0 8px rgba(0, 90, 156, 0.1); }

/* ══════════════════════════════════════════════
   CARTE DE PHASE (glassmorphism)
══════════════════════════════════════════════ */
.glass-card {
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(119, 33, 111, 0.14);
  border-radius: 18px;
  box-shadow: 0 6px 24px rgba(44, 0, 30, 0.07);
  transition: box-shadow 0.25s, border-color 0.25s;
}

.glass-card:hover {
  box-shadow: 0 10px 36px rgba(44, 0, 30, 0.12);
  border-color: rgba(119, 33, 111, 0.28);
}

.soc-phase-card {
  padding: 22px 24px;
}

.soc-phase-card__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

/* Badges de sévérité */
.severity-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.06em;
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: uppercase;
}

.severity-badge--critical { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; }
.severity-badge--high     { background: #fff4ef; color: #e95420; border: 1px solid rgba(233,84,32,0.3); }
.severity-badge--medium   { background: #f3e8f3; color: #77216f; border: 1px solid rgba(119,33,111,0.28); }
.severity-badge--info     { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }

.tool-tag {
  font-size: 11px;
  font-weight: 700;
  color: #5e2750;
  background: rgba(94, 39, 80, 0.08);
  border: 1px solid rgba(94, 39, 80, 0.18);
  padding: 4px 10px;
  border-radius: 20px;
  font-family: 'Ubuntu Mono', monospace;
}

.soc-phase-card__title {
  margin: 0 0 10px;
  font-size: 17px;
  font-weight: 800;
  color: #2c001e;
  letter-spacing: -0.01em;
  line-height: 1.3;
}

.soc-phase-card__body {
  margin: 0 0 14px;
  font-size: 14px;
  line-height: 1.65;
  color: var(--muted);
}

/* ══════════════════════════════════════════════
   BOX TERMINAL (dark code box)
══════════════════════════════════════════════ */
.soc-term-box {
  background: #1e1e1e;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 14px;
  border: 1px solid #2d2d2d;
}

.soc-term-box__bar {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 7px 12px;
  background: #111;
  border-bottom: 1px solid #2d2d2d;
}

.dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot--red    { background: #ff5f56; }
.dot--yellow { background: #ffbd2e; }
.dot--green  { background: #27c93f; }

.soc-term-box__label {
  font-family: 'Ubuntu Mono', monospace;
  font-size: 10px;
  color: #555;
  margin-left: 8px;
  flex: 1;
}

.soc-term-box__code {
  margin: 0;
  padding: 12px 14px;
  font-family: 'Ubuntu Mono', 'Fira Code', monospace;
  font-size: 12px;
  line-height: 1.5;
  color: #d4d4d4;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-x: auto;
}

.soc-term-box__code--modal {
  max-height: 360px;
  overflow-y: auto;
  font-size: 12.5px;
}

/* Bouton logs / playbooks */
.soc-detail-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  font-weight: 700;
  color: #77216f;
  background: rgba(119, 33, 111, 0.07);
  border: 1px solid rgba(119, 33, 111, 0.2);
  padding: 7px 14px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.soc-detail-btn:hover {
  background: rgba(119, 33, 111, 0.14);
  border-color: rgba(119, 33, 111, 0.36);
}

/* ══════════════════════════════════════════════
   BANDE KPIs
══════════════════════════════════════════════ */
.soc-results-band {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0;
  max-width: 900px;
  margin: 48px auto 32px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(119, 33, 111, 0.14);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 6px 24px rgba(44, 0, 30, 0.07);
}

.soc-kpi {
  flex: 1;
  min-width: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 22px 16px;
  border-right: 1px solid rgba(119, 33, 111, 0.1);
  text-align: center;
}

.soc-kpi:last-child { border-right: none; }

.soc-kpi__value {
  font-size: 26px;
  font-weight: 900;
  color: #e95420;
  line-height: 1;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
}

.soc-kpi__label {
  font-size: 11px;
  font-weight: 700;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  line-height: 1.3;
}

/* ══════════════════════════════════════════════
   CTA PDF
══════════════════════════════════════════════ */
.soc-footer-cta {
  text-align: center;
  margin-top: 8px;
}

.soc-pdf-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
}

/* ══════════════════════════════════════════════
   MODALE DÉTAIL
══════════════════════════════════════════════ */
.soc-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(30, 0, 20, 0.5);
  backdrop-filter: blur(6px);
  z-index: 1000;
  display: grid;
  place-items: center;
  padding: 24px;
}

.soc-modal {
  width: 100%;
  max-width: 680px;
  max-height: 88vh;
  overflow-y: auto;
  padding: 28px;
  background: rgba(255, 255, 255, 0.97);
}

.soc-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
}

.soc-modal__tool {
  font-size: 12px;
  font-weight: 700;
  color: #5e2750;
  background: rgba(94, 39, 80, 0.08);
  border: 1px solid rgba(94, 39, 80, 0.18);
  padding: 4px 10px;
  border-radius: 20px;
  font-family: 'Ubuntu Mono', monospace;
  margin-left: 8px;
}

.soc-modal__close {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: rgba(0, 0, 0, 0.06);
  border: none;
  cursor: pointer;
  color: var(--text);
  transition: background 0.2s;
}

.soc-modal__close:hover { background: rgba(0, 0, 0, 0.12); }

.soc-modal__title {
  margin: 0 0 10px;
  font-size: 20px;
  font-weight: 800;
  color: #2c001e;
}

.soc-modal__desc {
  margin: 0 0 18px;
  font-size: 15px;
  line-height: 1.65;
  color: var(--muted);
}

.soc-modal__details { margin-top: 18px; }

.soc-modal__details h4 {
  margin: 0 0 10px;
  font-size: 14px;
  font-weight: 800;
  color: #77216f;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.soc-modal__details ul {
  margin: 0;
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.soc-modal__details li {
  font-size: 14px;
  line-height: 1.5;
  color: var(--muted);
}

/* ══════════════════════════════════════════════
   TRANSITION MODALE
══════════════════════════════════════════════ */
.soc-modal-fade-enter-active,
.soc-modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.soc-modal-fade-enter-active .soc-modal,
.soc-modal-fade-leave-active .soc-modal {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.3s ease;
}

.soc-modal-fade-enter-from,
.soc-modal-fade-leave-to {
  opacity: 0;
}

.soc-modal-fade-enter-from .soc-modal,
.soc-modal-fade-leave-to .soc-modal {
  transform: translateY(24px) scale(0.97);
  opacity: 0;
}

/* ══════════════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════════════ */
@media (max-width: 720px) {
  .soc-phase-row {
    grid-template-columns: 40px 1fr;
    gap: 0 16px;
    margin-bottom: 40px;
  }

  .soc-center-line {
    left: 18px;
    transform: none;
  }

  /* Toutes les cartes à droite sur mobile */
  .soc-phase-row.phase-row--left .soc-phase-side--empty,
  .soc-phase-row.phase-row--right .soc-phase-side--empty {
    display: none;
  }

  .soc-phase-row.phase-row--left,
  .soc-phase-row.phase-row--right {
    grid-template-columns: 40px 1fr;
  }

  .soc-phase-row.phase-row--left .soc-phase-center  { order: 1; }
  .soc-phase-row.phase-row--left .soc-phase-side--content { order: 2; padding-right: 0; text-align: left; }
  .soc-phase-row.phase-row--right .soc-phase-center { order: 1; }
  .soc-phase-row.phase-row--right .soc-phase-side--content { order: 2; padding-left: 0; }

  .soc-phase-marker { width: 38px; height: 38px; }

  .soc-results-band { flex-wrap: wrap; }
  .soc-kpi { min-width: 45%; border-bottom: 1px solid rgba(119,33,111,0.1); }
}
</style>
