#!/usr/bin/env bash
set -e

# set up cron jobs for report generation
cat > /tmp/cronfile <<'EOF'
# Daily at 23:55
55 23 * * * cd /app && python reports/report_cli.py --period daily && \
  python reports/llm_analysis.py --period daily --summary-json '{"note":"(옵션)KPIs JSON"}' --outdir $(date -u +\%Y-\%m-\%d) && \
  python reports/github_push.py --src reports/$(date -u +\%Y-\%m-\%d)

# Weekly on Sundays at 23:57
57 23 * * 0 cd /app && python reports/report_cli.py --period weekly && \
  python reports/llm_analysis.py --period weekly --summary-json '{"note":"weekly KPIs"}' --outdir $(date -u +\%Y-\%m-\%d) && \
  python reports/github_push.py --src reports/$(date -u +\%Y-\%m-\%d)

# Monthly on the 1st at 00:10
10 0 1 * * cd /app && python reports/report_cli.py --period monthly && \
  python reports/llm_analysis.py --period monthly --summary-json '{"note":"monthly KPIs"}' --outdir $(date -u +\%Y-\%m-\%d) && \
  python reports/github_push.py --src reports/$(date -u +\%Y-\%m-\%d)
EOF

crontab /tmp/cronfile
cron -f
