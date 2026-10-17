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
        prompt=[
            {
                "role": "system",
                "content": (
                    "You are a supportive but honest habit coach. "
                    "I will give you the user's habit tracking data of some days ,maybe even 1 day,. "
                    "Using the provided data summarize their consistency, point out one specific pattern, and give one actionable piece of advice. "
                    "Keep it under 100 words. Do not use generic motivation.Also list the incompleted task name instead of id at the end and the benefit of doing them regularly."
                    "make the summary that is in points as human readable format."
                )
            },
            {
                "role": "user",
                "content": f"schedule of the user:{task}. Completed tasks id of each days:{checks}"
            }
        ]
        inputs=self.tokenizer.apply_chat_template(prompt,tokenize=True,add_generation_prompt=True,return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs=self.model.generate(**inputs,max_new_tokens=350,do_sample=True,temperature=0.15,top_p=0.85,repetition_penalty=1.1,)
        input_len=inputs["input_ids"].shape[1]
        output_tokens=outputs[0][input_len:]
        summary=self.tokenizer.decode(output_tokens,skip_special_tokens=True).strip()
        return summary