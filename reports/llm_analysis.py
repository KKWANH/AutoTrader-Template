# reports/llm_analysis.py
import argparse, os, json
from datetime import datetime
from pathlib import Path
import requests

def call_ollama(endpoint, model, prompt):
    r = requests.post(f"{endpoint}/api/generate",
                      json={"model":model,"prompt":prompt,"stream":False}, timeout=120)
    return r.json().get("response","").strip()

PROMPT_TMPL = """You are a trading performance analyst.
Summarize the period performance in bullet points. Then discuss:
- What worked / what failed
- Risk review (drawdown, variance)
- Suggestions (parameter/rule tweaks) as hypotheses only
- No trade commands.
Context(JSON):
{ctx}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--period", choices=["daily","weekly","monthly"], required=True)
    ap.add_argument("--summary-json", required=True)  # KPI/통계 JSON 파일(또는 문자열)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--ollama-endpoint", default=os.getenv("LLM_ENDPOINT","http://ollama:11434"))
    ap.add_argument("--model", default="phi3:mini")
    args = ap.parse_args()

    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    if os.path.exists(args.summary_json):
        ctx = open(args.summary_json,"r",encoding="utf-8").read()
    else:
        ctx = args.summary_json  # 직접 JSON 문자열 전달 가능

    prompt = PROMPT_TMPL.format(ctx=ctx)
    txt = call_ollama(args.ollama_endpoint, args.model, prompt)
    ts = datetime.utcnow().strftime("%Y-%m-%d")
    of = f"{args.outdir}/analysis_{args.period}_{ts}.md"
    with open(of,"w",encoding="utf-8") as f:
        f.write(f"# {args.period.capitalize()} LLM Analysis ({ts})\n\n")
        f.write(txt+"\n")
    print(f"[llm] analysis saved: {of}")

if __name__=="__main__":
    main()
