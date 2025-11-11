# Repository References

This document tracks the cloned repositories used as references for My Desk AI.

## Cloned Repositories

### Core Engine
- **crewai** - `/repos/crewai/`
  - GitHub: https://github.com/joaomdmoura/crewAI
  - Purpose: Main framework for building and managing agent teams
  - Used for: Agent orchestration, crew management

- **litellm** - `/repos/litellm/`
  - GitHub: https://github.com/BerriAI/litellm
  - Purpose: Magic translator box for 100+ LLMs
  - Used for: Model-agnostic LLM integration

- **langchain** - `/repos/langchain/`
  - GitHub: https://github.com/langchain-ai/langchain
  - Purpose: Underlying framework for crewai
  - Used for: LLM wrapper implementation

### Frontend
- **streamlit** - `/repos/streamlit/`
  - GitHub: https://github.com/streamlit/streamlit
  - Purpose: Browser-based dashboard framework
  - Used for: Phase 2 UI implementation

## Usage

These repositories are cloned for:
1. **Reference**: Understanding implementation details
2. **Documentation**: Access to source-level docs and examples
3. **Integration**: Deep understanding of APIs and patterns
4. **Debugging**: Tracing issues through source code

## Notes

- These are reference copies, not dependencies
- The actual packages are installed via pip in `venv/`
- Update repos periodically: `cd repos/<repo> && git pull`
- Check specific versions/tags if needed for compatibility

