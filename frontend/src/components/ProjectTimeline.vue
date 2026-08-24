<template>
  <div class="soc-implementation-container" ref="containerEl">
    <!-- Header inspiré de l'image 1 & 2 -->
    <header class="soc-header">
      <div class="soc-header__title-block">
        <h2 class="soc-title">SOC Open-Source Implementation</h2>
        <p class="soc-subtitle">
          Centre d'opérations de sécurité d'entreprise conçu et validé chez <strong>PANESS IT</strong> (Mémoire de fin de cycle IHTM — Samnick Biga Raoul Aubin).
        </p>
      </div>
      <div class="soc-header__tags">
        <span class="soc-pill soc-pill--orange">Wazuh v4.14.5</span>
        <span class="soc-pill soc-pill--aubergine">Suricata NIDS</span>
        <span class="soc-pill soc-pill--purple">DeepSeek AI</span>
        <span class="soc-pill soc-pill--blue">MISP & DFIR-IRIS</span>
        <span class="soc-pill soc-pill--green">Shuffle SOAR</span>
      </div>
    </header>

    <div class="soc-split-layout">
      <!-- COLONNE GAUCHE : TIMELINE CHRONOLOGIQUE -->
      <div class="soc-timeline-column">
        <div class="soc-timeline-track">
          <!-- Ligne verticale continue -->
          <div class="soc-vertical-line" aria-hidden="true"></div>

          <!-- Items de la timeline -->
          <div
            v-for="(step, idx) in socSteps"
            :key="step.id"
            class="soc-timeline-node"
            :class="[
              `soc-node--${step.severity.toLowerCase()}`,
              { 'soc-node--active': activeStepIndex === idx }
            ]"
            @click="selectStep(idx)"
            @mouseenter="hoverStep(idx)"
          >
            <!-- Badge icône circulaire lumineux sur la ligne -->
            <div class="soc-node-badge" :aria-label="step.title">
              <component :is="step.icon" :size="18" />
            </div>

            <!-- Carte de l'étape -->
            <div class="soc-node-card">
              <div class="soc-node-card__header">
                <h3 class="soc-node-card__title">{{ step.title }}</h3>
                <span
                  class="soc-severity-badge"
                  :class="`soc-severity-badge--${step.severity.toLowerCase()}`"
                >
                  {{ step.severity }}
                </span>
              </div>

              <p class="soc-node-card__description">{{ step.description }}</p>

              <!-- Terminal Code Box -->
              <div class="soc-terminal-box" v-if="step.codeSnippet">
                <div class="soc-terminal-box__bar" aria-hidden="true">
                  <span class="terminal-dot dot-red"></span>
                  <span class="terminal-dot dot-yellow"></span>
                  <span class="terminal-dot dot-green"></span>
                  <span class="terminal-title">{{ step.terminalTitle || 'console output' }}</span>
                </div>
                <pre class="soc-terminal-box__content"><code>{{ step.codeSnippet }}</code></pre>
              </div>

              <div class="soc-node-card__footer">
                <span class="soc-meta-tag"><Server :size="13" /> {{ step.vm }}</span>
                <span class="soc-meta-tag"><Layers :size="13" /> {{ step.phase }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- COLONNE DROITE : VISUALISATION INTERACTIVE -->
      <aside class="soc-visual-column" aria-label="Visualisation interactive du SOC">
        <div class="soc-visual-card">
          <div class="soc-visual-card__header">
            <div class="soc-visual-badge">
              <Activity :size="15" />
              <span>Interactive Visualization</span>
            </div>
            <div class="soc-visual-status">
              <span class="live-dot"></span>
              <span>Lab VirtualBox NAT (192.168.100.0/24)</span>
            </div>
          </div>

          <!-- Onglets de simulation -->
          <div class="soc-visual-tabs">
            <button
              v-for="tab in visualTabs"
              :key="tab.id"
              type="button"
              class="soc-visual-tab"
              :class="{ 'is-active': activeTab === tab.id }"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>

          <!-- CONTENU ONGLET 1 : TOPOLOGIE RÉSEAU & FLUX -->
          <div v-if="activeTab === 'topology'" class="soc-tab-content">
            <div class="soc-topology-grid">
              <div
                v-for="vm in virtualMachines"
                :key="vm.name"
                class="soc-vm-box"
                :class="{ 'soc-vm-box--highlighted': activeStepVMs.includes(vm.name) }"
              >
                <div class="soc-vm-box__header">
                  <span class="soc-vm-name">{{ vm.name }}</span>
                  <span class="soc-vm-ip">{{ vm.ip }}</span>
                </div>
                <div class="soc-vm-os">{{ vm.os }}</div>
                <div class="soc-vm-services">
                  <span v-for="service in vm.services" :key="service" class="soc-service-chip">
                    {{ service }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Détail du flux actif -->
            <div class="soc-flow-detail">
              <strong>Flux actif — {{ currentStep.title }}</strong>
              <p>{{ currentStep.flowDetail }}</p>
              <div class="soc-flow-pills">
                <span class="flow-pill">Source : {{ currentStep.flowSource }}</span>
                <span class="flow-arrow">→</span>
                <span class="flow-pill">Protocole : {{ currentStep.flowProto }}</span>
                <span class="flow-arrow">→</span>
                <span class="flow-pill">Cible : {{ currentStep.flowDest }}</span>
              </div>
            </div>
          </div>

          <!-- CONTENU ONGLET 2 : SCÉNARIOS D'ATTAQUE DU MÉMOIRE -->
          <div v-else-if="activeTab === 'scenarios'" class="soc-tab-content">
            <div class="soc-scenarios-list">
              <div
                v-for="(sc, sIdx) in attackScenarios"
                :key="sc.id"
                class="soc-scenario-item"
                :class="{ 'is-selected': selectedScenarioIndex === sIdx }"
                @click="selectedScenarioIndex = sIdx"
              >
                <div class="soc-scenario-item__header">
                  <span class="scenario-number">Scénario 0{{ sIdx + 1 }}</span>
                  <h4>{{ sc.title }}</h4>
                </div>
                <p class="scenario-desc">{{ sc.description }}</p>
                <div class="scenario-chain">
                  <span v-for="(node, nIdx) in sc.chain" :key="node" class="chain-node">
                    {{ node }}
                    <span v-if="nIdx < sc.chain.length - 1" class="chain-arrow">→</span>
                  </span>
                </div>
                <div class="scenario-result">
                  <CheckCircle2 :size="14" class="check-icon" />
                  <span><strong>Résultat validé :</strong> {{ sc.result }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- CONTENU ONGLET 3 : LOGS & PLAYBOOKS DU MÉMOIRE -->
          <div v-else class="soc-tab-content">
            <div class="soc-playbook-view">
              <div class="playbook-meta">
                <strong>Script / Règle :</strong> <code>{{ currentStep.scriptName || 'ossec.conf & local_rules.xml' }}</code>
                <span class="playbook-path">{{ currentStep.scriptPath }}</span>
              </div>
              <pre class="playbook-code"><code>{{ currentStep.playbookContent }}</code></pre>
            </div>
          </div>

          <!-- Bouton rapport complet -->
          <div class="soc-visual-footer">
            <div class="thesis-reference">
              <GraduationCap :size="16" />
              <span>Rapport de stage PANESS IT — Licence Pro RSI (IHTM)</span>
            </div>
            <a
              v-if="pdfUrl"
              :href="pdfUrl"
              target="_blank"
              rel="noreferrer"
              class="button primary button--sm"
            >
              <FileText :size="15" /> Consulter le mémoire PDF
            </a>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import {
  ShieldAlert,
  Cpu,
  Send,
  Radio,
  Terminal,
  Database,
  Server,
  Layers,
  Activity,
  CheckCircle2,
  GraduationCap,
  FileText,
} from 'lucide-vue-next';

defineProps({
  pdfUrl: {
    type: String,
    default: '',
  },
});

const activeStepIndex = ref(0);
const activeTab = ref('topology');
const selectedScenarioIndex = ref(0);

// Les étapes authentiques issues directement du mémoire de stage PANESS
const socSteps = [
  {
    id: 'fim-yara',
    title: 'FIM & YARA Active Response',
    severity: 'Critical',
    icon: ShieldAlert,
    vm: 'agent-linux / agent-windows',
    phase: 'Phase 4 & 6 — Surveillance & Détection Malware',
    description:
      'File Integrity Monitoring (FIM) surveillant les répertoires sensibles en temps réel. Déclenchement automatique du moteur YARA compilé avec les règles Valhalla pour scanner et identifier les malwares (ex. test EICAR).',
    terminalTitle: '/var/ossec/logs/active-responses.log',
    codeSnippet: `[INFO] YARA scan started on /home/raoulbiga/eicar_final6.txt
[ALERT] Rule 108001: YARA match: eicar_test
[ACTION] Triggering remove-threat.sh -> Malware successfully deleted`,
    flowDetail:
      'L\'agent FIM détecte la création de fichier -> Déclenche yara.sh -> Match règle Valhalla -> Suppression automatique par remove-threat.sh.',
    flowSource: 'agent-linux (192.168.100.30)',
    flowProto: 'Wazuh Active Response (1514 UDP)',
    flowDest: 'wazuh-server (192.168.100.10)',
    scriptName: 'remove-threat.sh & yara.sh',
    scriptPath: '/var/ossec/active-response/bin/',
    playbookContent: `#!/bin/bash
# Extrait du script yara.sh avec réponse active
YARA_PATH="/usr/local/bin/yara"
YARA_RULES="/var/ossec/active-response/yara/rules/yara_rules.yar"
FILENAME="$1"

YARA_OUTPUT=$("$YARA_PATH" -w -r -m "$YARA_RULES" "$FILENAME")
if [ -n "$YARA_OUTPUT" ]; then
  echo "wazuh-YARA: INFO - Scan result: $YARA_OUTPUT" >> /var/ossec/logs/active-responses.log
  rm -f "$FILENAME"
  echo "wazuh-YARA: INFO - Successfully deleted $FILENAME" >> /var/ossec/logs/active-responses.log
fi`,
  },
  {
    id: 'deepseek-shuffle',
    title: 'DeepSeek AI & Shuffle SOAR',
    severity: 'High',
    icon: Cpu,
    vm: 'soc-services (Docker)',
    phase: 'Phase 6 & 9 — Enrichissement IA & Orchestration',
    description:
      'Enrichissement contextuel par l\'IA DeepSeek pour expliquer l\'impact et les mesures de remédiation en langage clair. Orchestration des flux d\'analyse automatisés via les workflows Shuffle SOAR.',
    terminalTitle: 'Shuffle SOAR execution log (:3001)',
    codeSnippet: `[AI DEEPSEEK] Query sent with YARA description: 'EICAR Standard AV Test'
[RESPONSE] 'Fichier de test standard simulant une charge virale. Risque immédiat nul, supprimer le fichier.'
[SOAR] Shuffle webhook triggered -> VirusTotal reputation checked -> Clean verdict`,
    flowDetail:
      'Wazuh Manager envoie l\'alerte à l\'API DeepSeek -> Extrait les IOCs -> Exécute le workflow Shuffle SOAR -> Valide sur VirusTotal.',
    flowSource: 'wazuh-server (192.168.100.10)',
    flowProto: 'HTTPS REST API (:3001)',
    flowDest: 'soc-services Shuffle (:3001)',
    scriptName: 'custom-deepseek.py / Shuffle Workflow',
    scriptPath: '/var/ossec/integrations/custom-deepseek.py',
    playbookContent: `import requests, json, sys

def query_deepseek(description):
    headers = {"Authorization": "Bearer SK-DEEPSEEK-API-KEY", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": f"En un paragraphe, explique l'impact et la remédiation pour : {description}"}],
        "max_tokens": 256
    }
    r = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
    return r.json()['choices'][0]['message']['content']`,
  },
  {
    id: 'iris-telegram',
    title: 'IRIS Case Management & Telegram Alerting',
    severity: 'Medium',
    icon: Send,
    vm: 'soc-services & Wazuh Server',
    phase: 'Phase 8 & 9 — Gestion des Incidents & Alertes',
    description:
      'Création automatique de dossiers d\'incident structurés dans la plateforme DFIR-IRIS via webhook. Notification instantanée des analystes SOC sur smartphone via le bot Telegram dédié.',
    terminalTitle: 'Telegram Alerting Notification (Bot1)',
    codeSnippet: `[SOC PANESS] Alerte CRITIQUE (Niveau 12)
Règle: 100210 - Commande suspecte (netcat) exécutée
Agent: agent-linux (192.168.100.30) | Heure: 2026-06-29T14:42:53
[IRIS] Incident Case #2 créé automatiquement dans DFIR-IRIS`,
    flowDetail:
      'Alerte critique Wazuh (>= 10) -> Script custom-wazuh_iris.py -> Création dossier IRIS (:8443) -> custom-telegram.py -> Notification Bot1.',
    flowSource: 'wazuh-server (192.168.100.10)',
    flowProto: 'HTTPS Webhook (:8443 / Telegram API)',
    flowDest: 'DFIR-IRIS & Telegram Bot',
    scriptName: 'custom-telegram.py & custom-wazuh_iris.py',
    scriptPath: '/var/ossec/integrations/',
    playbookContent: `# Extrait de custom-telegram.py pour alertes PANESS
def format_alert(alert):
    rule = alert.get('rule', {})
    level = rule.get('level', 0)
    severity = "CRITIQUE" if level >= 12 else "ELEVE" if level >= 7 else "MOYEN"
    msg = f"*[SOC PANESS] Alerte {severity}*\n"
    msg += f"Règle: {rule.get('id')} (Niv.{level}) - {rule.get('description')}\n"
    msg += f"Agent: {alert.get('agent', {}).get('name')} ({alert.get('agent', {}).get('ip')})"
    return msg`,
  },
  {
    id: 'suricata-nids',
    title: 'Suricata NIDS Network Defense',
    severity: 'High',
    icon: Radio,
    vm: 'wazuh-server (Amazon Linux 2023)',
    phase: 'Phase 5 — Détection Réseau & Signatures ET',
    description:
      'Suricata NIDS inspectant le trafic réseau en temps réel sur l\'interface eth2. Règles Emerging Threats téléchargeables détectant les scans de ports, attaques SSH et exfiltrations suspectes.',
    terminalTitle: '/var/log/suricata/eve.json',
    codeSnippet: `[ALERT] ET SCAN Potential SSH Scan OUTBOUND
Src IP: 192.168.100.50 (kali-attacker) -> Dest IP: 192.168.100.30:22
[WAZUH] Rule 86601 triggered -> Nmap recognition pattern confirmed`,
    flowDetail:
      'Paquets réseau capturés sur eth2 -> Suricata génère eve.json -> Filebeat / Wazuh Agent lit eve.json -> Alerte dans Wazuh Dashboard.',
    flowSource: 'kali-attacker (192.168.100.50)',
    flowProto: 'TCP SYN / Nmap Reconnaissance',
    flowDest: 'agent-linux & wazuh-server',
    scriptName: 'suricata.yaml & rules',
    scriptPath: '/etc/suricata/',
    playbookContent: `# Configuration Suricata suricata.yaml
vars:
  address-groups:
    HOME_NET: "[192.168.100.0/24]"
    EXTERNAL_NET: "!$HOME_NET"

af-packet:
  - interface: eth2
    cluster-id: 99
    cluster-type: cluster_flow
    defrag: yes`,
  },
  {
    id: 'auditd-sysmon',
    title: 'Auditd & Sysmon Endpoint Visibility',
    severity: 'Critical',
    icon: Terminal,
    vm: 'agent-linux & agent-windows',
    phase: 'Phase 4 — Surveillance Terminaux & Listes CDB',
    description:
      'Auditd sous Linux et Sysmon sous Windows journalisant les exécutions de commandes et connexions suspectes. Comparaison instantanée avec la liste CDB suspicious-programs (/var/ossec/etc/lists/).',
    terminalTitle: 'Auditd & CDB Rule Matching',
    codeSnippet: `[AUDITD] execve() syscall captured: comm="nc" (netcat)
[CDB CHECK] Matched 'nc:red' in /var/ossec/etc/lists/suspicious-programs
[RULE 100210] Level 12 Alert fired: Suspicious command execution detected`,
    flowDetail:
      'Exécution commande suspecte -> Auditd/Sysmon -> Agent Wazuh -> Décodeur local -> Règle CDB -> Alerte niveau 12.',
    flowSource: 'agent-linux / agent-windows',
    flowProto: 'Auditd Syscall / EventChannel',
    flowDest: 'wazuh-server (192.168.100.10)',
    scriptName: 'suspicious-programs (CDB list) & local_rules.xml',
    scriptPath: '/var/ossec/etc/lists/ & rules/',
    playbookContent: `<!-- Règle locale dans local_rules.xml -->
<group name="auditd,sysmon,">
  <rule id="100210" level="12">
    <if_sid>80700</if_sid>
    <list field="audit.command" lookup="match_key">etc/lists/suspicious-programs</list>
    <description>Auditd: Commande suspecte détectée via liste CDB ($(audit.command))</description>
    <mitre>
      <id>T1059</id>
    </mitre>
  </rule>
</group>`,
  },
  {
    id: 'misp-threat-intel',
    title: 'MISP Threat Intelligence Correlation',
    severity: 'High',
    icon: Database,
    vm: 'soc-services (Docker :1443)',
    phase: 'Phase 7 — Threat Intelligence & Corrélation',
    description:
      'Base MISP partagée contenant les flux d\'IOCs malveillants. Corrélation automatique par script Python des adresses IP attaquant le serveur SSH ou le réseau.',
    terminalTitle: 'MISP IOC Correlation Engine',
    codeSnippet: `[SSH BRUTE FORCE] Multiple authentication failures from 192.168.100.50
[MISP QUERY] custom-misp.py checking IP against MISP threat feeds...
[IOC MATCH] IP flagged in malicious adversary campaign -> Escalated to IRIS`,
    flowDetail:
      'Tentatives d\'intrusion répétées -> Script custom-misp.py interroge l\'API MISP (:1443) -> Règle 100622 -> Signalement d\'IP malveillante.',
    flowSource: 'wazuh-server (192.168.100.10)',
    flowProto: 'HTTPS REST API (:1443)',
    flowDest: 'MISP Threat Sharing (:1443)',
    scriptName: 'custom-misp.py',
    scriptPath: '/var/ossec/integrations/custom-misp.py',
    playbookContent: `import requests, sys, json

def check_misp(ioc_value, ioc_type="ip-dst"):
    headers = {"Authorization": "MISP-API-KEY", "Accept": "application/json"}
    payload = {"returnFormat": "json", "value": ioc_value, "type": ioc_type}
    r = requests.post("https://192.168.100.20:1443/attributes/restSearch", headers=headers, json=payload, verify=False)
    data = r.json()
    return len(data.get('response', {}).get('Attribute', [])) > 0`,
  },
];

const visualTabs = [
  { id: 'topology', label: 'Topologie Réseau (5 VMs)' },
  { id: 'scenarios', label: 'Scénarios d\'Attaque (4 Tests)' },
  { id: 'playbooks', label: 'Playbooks & Scripts' },
];

const virtualMachines = [
  {
    name: 'wazuh-server',
    ip: '192.168.100.10',
    os: 'Amazon Linux 2023 (OVA)',
    services: ['Wazuh Manager :1514', 'OpenSearch :9200', 'Dashboard :443', 'Suricata NIDS'],
  },
  {
    name: 'soc-services',
    ip: '192.168.100.20',
    os: 'Ubuntu 24.04 (Docker)',
    services: ['MISP :1443', 'DFIR-IRIS :8443', 'Shuffle SOAR :3001', 'RabbitMQ / Postgres'],
  },
  {
    name: 'agent-linux',
    ip: '192.168.100.30',
    os: 'Debian 12',
    services: ['Wazuh Agent', 'Auditd', 'YARA v4.5.1', 'remove-threat.sh'],
  },
  {
    name: 'agent-windows',
    ip: '192.168.100.40',
    os: 'Windows 10 Pro',
    services: ['Wazuh Agent', 'Sysmon', 'YARA (yara64.exe)', 'yara.py'],
  },
  {
    name: 'kali-attacker',
    ip: '192.168.100.50',
    os: 'Kali Linux',
    services: ['Nmap Recon', 'SSH Brute Force', 'EICAR Payload', 'Exploits'],
  },
];

const attackScenarios = [
  {
    id: 'sc1',
    title: 'Scénario 1 : Détection et Réponse Malware',
    description: 'Dépôt d\'un fichier de test EICAR dans un dossier surveillé sur agent-linux.',
    chain: ['FIM Wazuh', 'YARA Valhalla', 'VirusTotal', 'DeepSeek AI', 'remove-threat.sh', 'Telegram & IRIS'],
    result: 'Fichier supprimé automatiquement en moins de 3 secondes, incident créé dans IRIS et alerté sur Telegram.',
  },
  {
    id: 'sc2',
    title: 'Scénario 2 : Balayage et Reconnaissance Réseau',
    description: 'Scan agressif Nmap (-A) lancé depuis kali-attacker vers les terminaux internes.',
    chain: ['Scan Nmap (Kali)', 'Suricata NIDS (eth2)', 'Règle ET SCAN 86601', 'Alerte Wazuh', 'IRIS Case'],
    result: 'Détection instantanée des signatures réseau, catégorisation en reconnaissance et alerte analyste.',
  },
  {
    id: 'sc3',
    title: 'Scénario 3 : Commande Suspecte sous Linux',
    description: 'Exécution d\'un binaire non autorisé (nc / netcat) sur l\'agent Debian.',
    chain: ['nc exécuté', 'Auditd Journalisation', 'Liste CDB suspicious-programs', 'Règle 100210 (Niv.12)', 'Telegram Bot'],
    result: 'Alerte critique niveau 12 déclenchée immédiatement avec notification prioritaire envoyée au SOC.',
  },
  {
    id: 'sc4',
    title: 'Scénario 4 : Attaque par Force Brute SSH',
    description: 'Multiples tentatives de connexion SSH avec identifiants invalides depuis Kali.',
    chain: ['Brute Force SSH', 'Règle 5710 Wazuh', 'Script custom-misp.py', 'Corrélation IOC MISP', 'Ticket IRIS'],
    result: 'IP attaquante identifiée et corrélée avec la base de menaces MISP, consolidation dans le dossier d\'incident.',
  },
];

const currentStep = computed(() => socSteps[activeStepIndex.value] || socSteps[0]);

const activeStepVMs = computed(() => {
  const step = currentStep.value;
  if (!step) return [];
  const vmStr = step.vm.toLowerCase();
  const matched = [];
  if (vmStr.includes('wazuh')) matched.push('wazuh-server');
  if (vmStr.includes('soc-services') || vmStr.includes('docker')) matched.push('soc-services');
  if (vmStr.includes('linux')) matched.push('agent-linux');
  if (vmStr.includes('windows')) matched.push('agent-windows');
  if (step.flowSource.includes('kali') || step.title.toLowerCase().includes('nmap')) matched.push('kali-attacker');
  return matched.length ? matched : ['wazuh-server'];
});

function selectStep(index) {
  activeStepIndex.value = index;
}

function hoverStep(index) {
  activeStepIndex.value = index;
}
</script>

<style scoped>
.soc-implementation-container {
  width: 100%;
  margin: 0 auto;
  font-family: inherit;
  color: var(--text);
}

/* Header */
.soc-header {
  padding: 0 0 24px;
  border-bottom: 1px solid var(--outline);
  margin-bottom: 32px;
}

.soc-title {
  color: #8c2d19; /* Teinte rouille/aubergine comme sur l'image 1 */
  font-size: clamp(24px, 3.2vw, 34px);
  font-weight: 800;
  letter-spacing: -0.015em;
  margin: 0 0 8px;
}

.soc-subtitle {
  color: var(--muted);
  font-size: 16px;
  line-height: 1.6;
  max-width: 900px;
  margin: 0 0 16px;
}

.soc-header__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.soc-pill {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 12px;
  border: 1px solid transparent;
}

.soc-pill--orange { background: rgba(233, 84, 32, 0.1); color: #e95420; border-color: rgba(233, 84, 32, 0.25); }
.soc-pill--aubergine { background: rgba(119, 33, 111, 0.1); color: #77216f; border-color: rgba(119, 33, 111, 0.25); }
.soc-pill--purple { background: rgba(122, 61, 184, 0.1); color: #7a3db8; border-color: rgba(122, 61, 184, 0.25); }
.soc-pill--blue { background: rgba(0, 90, 156, 0.1); color: #005a9c; border-color: rgba(0, 90, 156, 0.25); }
.soc-pill--green { background: rgba(31, 122, 63, 0.1); color: #1f7a3f; border-color: rgba(31, 122, 63, 0.25); }

/* Split Layout */
.soc-split-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(360px, 0.95fr);
  gap: 36px;
  align-items: start;
}

@media (max-width: 980px) {
  .soc-split-layout {
    grid-template-columns: 1fr;
  }
}

/* Timeline Column */
.soc-timeline-column {
  position: relative;
}

.soc-timeline-track {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* Ligne continue */
.soc-vertical-line {
  position: absolute;
  top: 24px;
  bottom: 24px;
  left: 20px;
  width: 2.5px;
  background: linear-gradient(180deg, #e95420 0%, #77216f 60%, #c48abc 100%);
  border-radius: 2px;
  z-index: 1;
}

/* Node Item */
.soc-timeline-node {
  position: relative;
  display: flex;
  gap: 20px;
  align-items: flex-start;
  z-index: 2;
  cursor: pointer;
  transition: transform 0.25s ease;
}

.soc-timeline-node:hover {
  transform: translateX(4px);
}

/* Badge Icone Lumineux */
.soc-node-badge {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #ffffff;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border: 2.5px solid;
  box-shadow: 0 4px 12px rgba(44, 0, 30, 0.1);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s;
}

.soc-node--critical .soc-node-badge {
  border-color: #e95420;
  color: #e95420;
}

.soc-node--high .soc-node-badge {
  border-color: #77216f;
  color: #77216f;
}

.soc-node--medium .soc-node-badge {
  border-color: #005a9c;
  color: #005a9c;
}

.soc-node--active .soc-node-badge {
  transform: scale(1.15);
  box-shadow: 0 0 0 6px rgba(233, 84, 32, 0.18);
  background: #fff;
}

/* Carte de l'étape */
.soc-node-card {
  flex: 1;
  background: #ffffff;
  border: 1px solid rgba(119, 33, 111, 0.14);
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0 4px 18px rgba(44, 0, 30, 0.05);
  transition: border-color 0.25s, box-shadow 0.25s;
}

.soc-node--active .soc-node-card {
  border-color: rgba(233, 84, 32, 0.55);
  box-shadow: 0 8px 26px rgba(233, 84, 32, 0.12);
}

.soc-node-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.soc-node-card__title {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: var(--aubergine-dark);
}

/* Badges de sévérité pastel */
.soc-severity-badge {
  font-size: 11px;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 20px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.soc-severity-badge--critical {
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fca5a5;
}

.soc-severity-badge--high {
  background: #fce7f3;
  color: #be185d;
  border: 1px solid #fbcfe8;
}

.soc-severity-badge--medium {
  background: #e0f2fe;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.soc-node-card__description {
  margin: 0 0 12px;
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
}

/* Boîte Terminal Code (Dark Box avec output) */
.soc-terminal-box {
  background: #2b2b2b;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
  border: 1px solid #3d3d3d;
}

.soc-terminal-box__bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #1e1e1e;
  border-bottom: 1px solid #333;
}

.terminal-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.dot-red { background: #ff5f56; }
.dot-yellow { background: #ffbd2e; }
.dot-green { background: #27c93f; }

.terminal-title {
  color: #888;
  font-size: 10px;
  font-family: monospace;
  margin-left: 6px;
}

.soc-terminal-box__content {
  margin: 0;
  padding: 10px 12px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Ubuntu Mono', monospace;
  font-size: 12px;
  line-height: 1.5;
  color: #e6e6e6;
  white-space: pre-wrap;
  word-break: break-all;
}

.soc-node-card__footer {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.soc-meta-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: #777;
  font-weight: 600;
}

/* Colonne Droite : Visualisation Interactive */
.soc-visual-column {
  position: sticky;
  top: 96px;
}

.soc-visual-card {
  background: #ffffff;
  border: 1px solid rgba(119, 33, 111, 0.16);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(44, 0, 30, 0.07);
}

.soc-visual-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--outline);
}

.soc-visual-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--aubergine-dark);
  font-weight: 800;
  font-size: 15px;
}

.soc-visual-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #666;
}

.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3);
  animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
  70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Onglets */
.soc-visual-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 18px;
}

.soc-visual-tab {
  flex: 1;
  padding: 8px 10px;
  font-size: 12px;
  font-weight: 700;
  border-radius: 10px;
  border: 1px solid var(--outline);
  background: #f8f6f8;
  color: var(--muted);
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.soc-visual-tab.is-active {
  background: var(--aubergine-dark);
  color: #fff;
  border-color: var(--aubergine-dark);
  box-shadow: 0 2px 8px rgba(119, 33, 111, 0.25);
}

/* Topologie 5 VMs */
.soc-topology-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 18px;
}

.soc-vm-box {
  background: #faf8fa;
  border: 1px solid var(--outline);
  border-radius: 12px;
  padding: 12px;
  transition: all 0.3s;
}

.soc-vm-box--highlighted {
  border-color: #e95420;
  background: #fff6f3;
  box-shadow: 0 0 0 2px rgba(233, 84, 32, 0.25);
  transform: translateY(-2px);
}

.soc-vm-box__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.soc-vm-name {
  font-weight: 800;
  font-size: 13px;
  color: var(--aubergine-dark);
}

.soc-vm-ip {
  font-size: 11px;
  font-family: monospace;
  color: #666;
}

.soc-vm-os {
  font-size: 11px;
  color: var(--muted);
  margin-bottom: 6px;
}

.soc-vm-services {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.soc-service-chip {
  font-size: 10px;
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 6px;
  color: #444;
}

/* Flux actif detail */
.soc-flow-detail {
  background: #fdfbfd;
  border: 1px solid var(--outline);
  border-radius: 12px;
  padding: 14px;
  font-size: 13px;
  line-height: 1.5;
  margin-bottom: 18px;
}

.soc-flow-detail strong {
  display: block;
  color: var(--aubergine-dark);
  margin-bottom: 4px;
}

.soc-flow-detail p {
  margin: 0 0 10px;
  color: var(--muted);
}

.soc-flow-pills {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  font-size: 11px;
}

.flow-pill {
  background: #eee5ed;
  padding: 3px 8px;
  border-radius: 6px;
  color: var(--aubergine-dark);
  font-weight: 600;
}

.flow-arrow {
  color: #e95420;
  font-weight: 900;
}

/* Scenarios Tab */
.soc-scenarios-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 18px;
}

.soc-scenario-item {
  border: 1px solid var(--outline);
  border-radius: 12px;
  padding: 12px 14px;
  background: #faf8fa;
  cursor: pointer;
  transition: all 0.2s;
}

.soc-scenario-item.is-selected {
  border-color: #e95420;
  background: #fff7f4;
  box-shadow: 0 2px 10px rgba(233, 84, 32, 0.12);
}

.soc-scenario-item__header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.scenario-number {
  font-size: 10px;
  font-weight: 800;
  background: #e95420;
  color: #fff;
  padding: 2px 6px;
  border-radius: 4px;
}

.soc-scenario-item__header h4 {
  margin: 0;
  font-size: 13px;
  font-weight: 700;
  color: var(--aubergine-dark);
}

.scenario-desc {
  margin: 0 0 8px;
  font-size: 12px;
  color: var(--muted);
}

.scenario-chain {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
  font-size: 10px;
  font-weight: 600;
  color: var(--aubergine-dark);
  margin-bottom: 6px;
}

.chain-arrow {
  color: #e95420;
}

.scenario-result {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #15803d;
  background: #f0fdf4;
  padding: 4px 8px;
  border-radius: 6px;
}

/* Playbooks Tab */
.soc-playbook-view {
  background: #2b2b2b;
  border-radius: 12px;
  padding: 14px;
  color: #fff;
  margin-bottom: 18px;
}

.playbook-meta {
  font-size: 11px;
  color: #bbb;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 4px;
}

.playbook-meta code {
  color: #fca886;
  font-weight: 700;
}

.playbook-path {
  font-family: monospace;
  color: #888;
}

.playbook-code {
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  line-height: 1.45;
  color: #d4d4d4;
  overflow-x: auto;
  max-height: 280px;
}

/* Footer & Bouton PDF */
.soc-visual-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  padding-top: 14px;
  border-top: 1px solid var(--outline);
}

.thesis-reference {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--muted);
  font-weight: 600;
}

.button--sm {
  padding: 8px 14px;
  font-size: 13px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
</style>
