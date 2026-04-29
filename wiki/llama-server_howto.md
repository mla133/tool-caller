# llama-server CLI howto notes/instructions

## Invoking the embeddings to use GPU
```
./llama-server \

  -m models/nomic-embed-text-v1.5.Q4_K_M.gguf \
  --port 8124 \
  --host 127.0.0.1 \
  --embedding \
  -ngl 99 \
  --dev Vulkan0
```
## Test using Powershell
```PowerShell
Invoke-RestMethod -Uri http://localhost:8124/v1/embeddings -Method Post -ContentType "application/json" -Body '{"input": "search_query: What is the capital of France?", "model": "nomic-embed-text"}'
```
This should return without error.  To inspect the embeddings in readable JSON:
```
Invoke-RestMethod -Uri http://localhost:8124/v1/embeddings -Method Post -ContentType "application/json" -Body '{"input": "search_query: test", "model": "nomic-embed-text"}' | ConvertTo-Json -Depth 10 | Out-File "pretty_output.json"
```
