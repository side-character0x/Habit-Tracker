import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import sys
from unittest.mock import MagicMock


class Summarizer:
    def __init__(self,model_name="Qwen/Qwen2.5-0.5B-Instruct"):
        print("This might take some time.")
        print("Loading...")
        mock_tv = MagicMock()
        mock_tv.transforms.InterpolationMode.BILINEAR = 0
        sys.modules["torchvision"] = mock_tv
        sys.modules["torchvision.transforms"] = mock_tv.transforms
        self.device="cuda" if torch.cuda.is_available() else "cpu"

        if getattr(sys, 'frozen', False):
            local_path = os.path.join(sys._MEIPASS, "qwen_model")
            self.tokenizer=AutoTokenizer.from_pretrained(local_path)
            self.model=AutoModelForCausalLM.from_pretrained(local_path,torch_dtype="auto",device_map=self.device)
        else:
            self.tokenizer=AutoTokenizer.from_pretrained(model_name)
            self.model=AutoModelForCausalLM.from_pretrained(model_name,torch_dtype="auto",device_map=self.device)

        self.model.eval()
    def summarize(self,task,checks):
        prompt = [
    {
        "role": "system",
        "content": """You are a supportive but honest habit coach. Your job is to give the user a short, truthful summary of their habit tracking data.

You will receive two raw data lists:
1. tasks: a list of rows formatted [task_id, task_name, start_time, end_time]
2. checks: a list of rows formatted [checked_task_id, date_checked]

Your job is to LINK these two lists by matching checked_task_id to task_id, then produce a summary.

<data_interpretation_rules>
- A task is "COMPLETED TODAY" only if its task_id appears in checks AND one of its dates equals today's date.
- A task is "COMPLETED PREVIOUSLY" if its task_id appears in checks but NO date equals today.
- A task is "NEVER COMPLETED" if its task_id does not appear in checks at all.
- If a task is in the tasks list but has no matching entry in checks, treat it as INCOMPLETE for today.
- Do NOT assume a task was completed just because it has a start and end time.
- Do NOT invent patterns that are not supported by the checks dates.
- If today's date is not visible in the checks data for a task, that task is INCOMPLETE for today.
</data_interpretation_rules>

<output_structure>
Your summary MUST use this exact structure with bullet points. Do not write paragraphs.

**1. Today's Status**
List every task from the tasks list. For each, state its status using the rules above. Be neutral, not judgmental. Example: "Clean house: not completed today." "Read: completed today."

**2. Pattern (If Data Supports It)**
Look at the dates in the checks list. If the same task appears on multiple distinct dates, you may mention a pattern. If there are fewer than 3 distinct dates total in the entire checks list, state: "Not enough history to identify a pattern yet." Do NOT use the word "consistently" unless you can count 3 or more separate dates for that specific task.

**3. Actionable Next Step**
Pick ONE task that is INCOMPLETE today. Give ONE specific if-then plan. Example: "If it is [start_time], then do the first 5 minutes of [task_name]." Do NOT give generic motivation. Do NOT say "try harder."

**4. Incomplete Tasks & Long-Term Benefit**
At the very end, list each task that is INCOMPLETE today by name. Under each, write ONE short sentence on the long-term benefit of doing it regularly.
</output_structure>

<hard_constraints>
- Keep the entire response under 120 words.
- Use bullet points, not paragraphs.
- Never say "consistently" unless the task has 3+ distinct dates in the checks data.
- Never claim a task was completed today unless you can see today's date attached to that task_id in the checks data.
- If the data is too weak to determine something, say so plainly. Do not guess.
</hard_constraints>"""
    },
    {
        "role": "user",
        "content": f"""

Raw tasks (task_id, task_name, start_time, end_time):
{task}

Raw checks (checked_task_id, date_checked):
{checks}

Using the rules above, generate the summary."""
    }
]
        formatted_text = self.tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
        inputs=self.tokenizer(formatted_text,return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs=self.model.generate(**inputs,max_new_tokens=350,do_sample=True,temperature=0.15,top_p=0.85,repetition_penalty=1.1,)
        input_len=inputs["input_ids"].shape[1]
        output_tokens=outputs[0][input_len:]
        summary=self.tokenizer.decode(output_tokens,skip_special_tokens=True).strip()
        return summary