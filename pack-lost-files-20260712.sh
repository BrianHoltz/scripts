#!/usr/bin/env bash
set -euo pipefail

user_home=""
archive="lost-files-20260712.tar.gz"
skip_gdrive=0
debug=0

for arg in "$@"; do
  case "$arg" in
    -x)
      debug=1
      ;;
    --skip-gdrive)
      skip_gdrive=1
      ;;
    /*)
      user_home="$arg"
      ;;
    *)
      archive="$arg"
      ;;
  esac
done

if [[ $debug -eq 1 ]]; then
  set -x
fi

if [[ -z "$user_home" ]]; then
  echo "Usage: $0 [-x] USER_HOME [ARCHIVE] [--skip-gdrive]" >&2
  echo "  -x enables debug output (set -x)" >&2
  echo "  USER_HOME is /Users/brian or /Volumes/backup/Users/brian" >&2
  echo "  ARCHIVE defaults to lost-files-20260712.tar.gz" >&2
  echo "  --skip-gdrive omits all gdrive/* entries (dangling symlinks)" >&2
  exit 2
fi

docs_files=(
  "Documents/HoltzDotOrg/PurissimaWater/2026-07/00 Notes.md"
  "Documents/.github/copilot-instructions.md"
  "Documents/.gitignore"
  "Documents/GitScheme.md"
  "Documents/HoltzDotOrg/.htaccess"
  "Documents/HoltzDotOrg/404.shtml"
  "Documents/HoltzDotOrg/PurissimaWater/CommsPolicy.md"
  "Documents/HoltzDotOrg/PurissimaWater/PHWD.md"
  "Documents/HoltzDotOrg/Thoughts/KnowingHumans/blogtoc.js"
  "Documents/README.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/.gitignore"
  "Documents/HoltzDotOrg/Thoughts/wiki/.htaccess"
  "Documents/HoltzDotOrg/Thoughts/wiki/BrianThinks.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/BrianThinks.py"
  "Documents/HoltzDotOrg/Thoughts/wiki/BrianThinksGPT.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/BrianThinksMore.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/BrianThinksTemplate.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/EpistemicEvalTemplate.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/HowIUseAI.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/Makefile"
  "Documents/HoltzDotOrg/Thoughts/wiki/PredictItPredictions.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/ai-economic-evals.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/ai-predictions.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/alien-impacts.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/alien-theories.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/alien-theorists.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/alien-witnesses.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/bibliography.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/capacity-disruptions.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/comparative-development-biblio.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/comparative-development-gemini.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/comparative-development-tagging.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/comparative-development.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/config.json"
  "Documents/HoltzDotOrg/Thoughts/wiki/conspiracy-theories.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/evaluations/20260322_HoganKnightsTemplar.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/evaluations/20260322_HoganKnightsTemplar/Hogan.txt"
  "Documents/HoltzDotOrg/Thoughts/wiki/evaluations/20260322_HoganKnightsTemplar/Hogan_diarized.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/evaluations/20260322_HoganKnightsTemplar/Hogan_diarized_ts.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/evaluations/20260322_HoganKnightsTemplar/diarize.py"
  "Documents/HoltzDotOrg/Thoughts/wiki/evaluations/index.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/goods-classification-history.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/index.html"
  "Documents/HoltzDotOrg/Thoughts/wiki/index.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/navigation.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/rent-seekers.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/sowell-eval-gpt41.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/sowell-gemini3pro.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/sowell-gpt41.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/sowell-gpt4o.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/sowell-gpt5mini.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/sowell-grokcodefast1.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/sowell-opus45.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/sowell-sonnet.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/sowell-synthesis-gpt41.md"
  "Documents/HoltzDotOrg/Thoughts/wiki/super-intelligence.md"
)

gdrive_files=(
  "gdrive/FamilyDocuments/Genealogy/Holtz/1975-12-11 Jerry Holtz roast.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/2026-05-05_sublease_agreement_Heather-Junyi_deprecated.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/2026-05-05_sublease_agreement_Heather-Junyi_official.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/2026-06-25 555Ten Jun rent 1.png"
  "gdrive/FamilyDocuments/Heather/2026 NYC/2026-06-25 555Ten Jun rent 2.png"
  "gdrive/FamilyDocuments/Heather/2026 NYC/2026-06-25 555Ten Jun rent 3.png"
  "gdrive/FamilyDocuments/Heather/2026 NYC/2026-06-25 555Ten Jun rent 4.png"
  "gdrive/FamilyDocuments/Heather/2026 NYC/2026-06-25 555Ten Jun rent all.png"
  "gdrive/FamilyDocuments/Heather/2026 NYC/225Cherry.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/555Ten.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/555TenSubleasing.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/AGENTS.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/ApartmentSearch.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/ApartmentsByHDH.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/CORT_Lease_Documents signed.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/ChatGPT_thread.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/Cort June Autopay Receipt.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/Cort furniture lease Holtz L1544502.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/Cort furniture order.txt"
  "gdrive/FamilyDocuments/Heather/2026 NYC/EugeneFlr55.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/IncomeVerification/2024 Brian taxes.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/IncomeVerification/20240407 BH driver license.jpg"
  "gdrive/FamilyDocuments/Heather/2026 NYC/IncomeVerification/2025 Brian taxes.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/IncomeVerification/Brian Fidelity Statement 2026-03.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/IncomeVerification/Brian Fidelity Statement 2026-04.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/IncomeVerification/Brian Portfolio Balances.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/IncomeVerification/Brian Walmart employment.pdf"
  "gdrive/FamilyDocuments/Heather/2026 NYC/OhanaCandidates.md"
  "gdrive/FamilyDocuments/Heather/2026 NYC/chats/2026.04.29.Wed_Ohana_Yao_Sublease-thread.txt"
  "gdrive/FamilyDocuments/Heather/2026 NYC/chats/2026.05.04.Mon_Email_CORT_Forwarded-furniture-order-thread.txt"
  "gdrive/FamilyDocuments/Heather/2026 NYC/chats/2026.05.04.Mon_Family_Heather_Sublease-options-chat.txt"
  "gdrive/FamilyDocuments/Heather/2026 NYC/chats/2026.05.05.Tue_Ohana_Junyi_Sublease-booking-and-move-in.txt"
  "gdrive/FamilyDocuments/Heather/2026 NYC/chats/2026.05.07.Thu_Ohana_Junyi_Building-application-followup.txt"
  "gdrive/FamilyDocuments/Heather/2026 NYC/chats/2026.05.16.Sat_Email_CORT_Clarification-extra-items.txt"
  "gdrive/FamilyDocuments/Logs/Log Brian.txt"
  "gdrive/FamilyDocuments/Logs/Log Family Computers.txt"
  "gdrive/FamilyDocuments/Logs/Log Family Travel.md"
  "gdrive/FamilyDocuments/Logs/Log Family.txt"
  "gdrive/FamilyDocuments/Logs/Log HDH Bank.txt"
  "gdrive/FamilyDocuments/Logs/Log Holtzes.md"
  "gdrive/FamilyDocuments/Logs/Log Jacqueline.txt"
  "gdrive/FamilyDocuments/Logs/Log Lusins.txt"
  "gdrive/FamilyDocuments/Logs/Log Melisse.txt"
  "gdrive/FamilyDocuments/Logs/LogsObsolete/Log Holtzes obsolete 2021.txt"
  "gdrive/FamilyDocuments/Logs/LogsObsolete/Log Holtzes obsolete 2026.txt"
  "gdrive/FamilyDocuments/Logs/LogsObsolete/Log Holtzes obsolete.txt"
  "gdrive/FamilyDocuments/Logs/LogsObsolete/Log Holtzes.txt"
  "gdrive/.gitignore"
  "gdrive/FamilyDocuments/Brian/BrianMedicalHistory.md"
  "gdrive/FamilyDocuments/Brian/BrianMedicalHistoryPrompt.md"
  "gdrive/FamilyDocuments/FamilyEncyclopedia.md"
  "gdrive/FamilyDocuments/FamilyEncyclopedia.py"
  "gdrive/FamilyDocuments/FamilyManual.md"
  "gdrive/FamilyDocuments/Genealogy/FamilyTree.md"
  "gdrive/FamilyDocuments/Genealogy/FamilyTree.py"
  "gdrive/FamilyDocuments/Genealogy/FamilyTreeProject.md"
  "gdrive/FamilyDocuments/Genealogy/FamilyTreeProjectLog.md"
  "gdrive/FamilyDocuments/Genealogy/Lusin/PatKaiserAncestry.md"
  "gdrive/README.md"
  "gdrive/Workspaces-template.code-workspace"
)

tmp_list=$(mktemp)
trap 'rm -f "$tmp_list"' EXIT

for rel in "${docs_files[@]}"; do
  src="$user_home/$rel"
  if [[ ! -e "$src" ]]; then
    echo "warning: missing $src" >&2
  else
    printf '%s\n' "$rel" >> "$tmp_list"
  fi
done

if [[ $skip_gdrive -eq 0 ]]; then
  for rel in "${gdrive_files[@]}"; do
    src="$user_home/$rel"
    if [[ ! -e "$src" ]]; then
      echo "warning: missing $src" >&2
    else
      printf '%s\n' "$rel" >> "$tmp_list"
    fi
  done
fi

tar -C "$user_home" -czf "$archive" -T "$tmp_list"
echo "Wrote $archive"
