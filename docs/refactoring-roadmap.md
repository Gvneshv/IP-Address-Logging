# 🗺️ Project Roadmap

| Stage | Status | Goals | Note |
| :--- | :---: | :--- | :--- |
| **🎯 Phase 1: Foundation & Audit** | ✅ | [ ✓ ] Create architecture document</br>[ ✓ ] Audit existing codebase</br>[ ✓ ] Identify collection pipeline</li> | Base for refactoring |
| **🏗️ Phase 2: Abstraction Layer** | ✅ | [ ✓ ] Introduce router collector (orchestrator + provider interface)</br>[ ✓ ] Extend snapshot schema (event["network"]["router"], populated when non-empty)</br>[ ✓ ] Add WAN change detection</br>[ ✓ ] Add configuration for notification trigger (notifications.notify_on)</br>  | Detection logic is ready but has nothing real to compare yet - AutoDetectionProvider.collect() still returns {} |
| **🔌 Phase 3: Integrations & Features** | ⏳ | [&emsp;] Introduce Router integrations</br>[&emsp;] Add WAN provider</br>[&emsp;] Add capability detection</br> | Functionality expansion |
| **📝 Phase 4: Documentation & Community** | ⏳ | [&emsp;] Update documentation</br>[&emsp;] Add contributor guidelines</br> | Final |