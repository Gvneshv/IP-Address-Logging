# 🗺️ Project Roadmap

| Stage | Status | Goals | Note |
| :--- | :---: | :--- | :--- |
| **🎯 Phase 1: Foundation & Audit** | ✅ | [ ✓ ] Create architecture document</br>[ ✓ ] Audit existing codebase</br>[ ✓ ] Identify collection pipeline</li> | Base for refactoring |
| **🏗️ Phase 2: Abstraction Layer** | ✅ | [ ✓ ] Introduce router collector (orchestrator + provider interface)</br>[ ✓ ] Extend snapshot schema (event["network"]["router"], populated when non-empty)</br>[ ✓ ] Add WAN change detection</br>[ ✓ ] Add configuration for notification trigger (notifications.notify_on)</br>  | Detection logic is ready but has nothing real to compare yet - AutoDetectionProvider.collect() still returns {} |
| **🔌 Phase 3: Integrations & Features** | 🔄 | [ ✓ ] Introduce Router integrations (TplinkProvider)</br>[ ✓ ] Add WAN provider (TP-Link, via tplinkrouterc6u)</br>[ ✓ ] Add capability detection (CLI diagnostic output, not persisted)</br> | MikroTik and other vendors remain unimplemented and untestable without hardware - flagged, not attempted |
| **📝 Phase 4: Documentation & Community** | ⏳ | [&emsp;] Update documentation</br>[&emsp;] Add contributor guidelines</br> | Final |