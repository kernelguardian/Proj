from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from fastapi import FastAPI, WebSocket

app = FastAPI()


# LLAMA2 Model
# Load the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("kernelguardian/instruct2action_llama2")
model = AutoModelForCausalLM.from_pretrained("kernelguardian/instruct2action_llama2")


# T5 Model
tokenizer = AutoTokenizer.from_pretrained("kernelguardian/flant5action")
model = AutoModelForCausalLM.from_pretrained("kernelguardian/flant5action")



@app.post("/generate_text/")
async def generate_text(data: dict):
    try:
        # Extract text from the JSON request
        input_text = data["input_text"]

        # Tokenize the input text
        input_ids = tokenizer.encode(input_text, return_tensors="pt")

        # Generate text using the model
        with torch.no_grad():
            output = model.generate(input_ids, max_length=50, num_return_sequences=1)
        
        # Decode the generated output
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

        return {"generated_text": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_text()
            input_text = data.strip()

            # Tokenize the input text
            input_ids = tokenizer.encode(input_text, return_tensors="pt")

            # Generate text using the model
            with torch.no_grad():
                output = model.generate(input_ids, max_length=50, num_return_sequences=1)
            
            # Decode the generated output
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

            await websocket.send_text(generated_text)

        except WebSocketDisconnect:
            break