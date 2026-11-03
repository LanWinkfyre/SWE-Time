# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
inline::sqlite-vec missing WAL mode and busy_timeout on vector store connections

### System Info

- llama-stack version: latest main                              
- Python: 3.12                                                                          
- OS: Linux (UBI9)                                              
- Deployment: Kubernetes, multiple uvicorn workers         

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

### Bug Description                                                                     

The inline::sqlite-vec provider opens database connections without setting WAL mode or busy_timeout. With multiple uvicorn workers, concurrent writes fail immediately with `sqlite3.OperationalError: database is locked` instead of waiting and retrying.       
                                                                  
The KV store (`src/llama_stack/core/storage/sqlstore/sqlalchemy_sqlstore.py:140-145`) already handles this correctly by setting `journal_mode=WAL`, `busy_timeout=5000`, and `synchronous=NORMAL`. The vector store at `src/llama_stack/providers/inline/vector_io/sqlite_vec/sqlite_vec.py:111` does not.

### Steps to Reproduce                                                                  

Create a run config with 2 workers:                                                     

`run.yaml`                                                                  
```yaml                                                                                 
server:                                                         
  port: 8321                                                                            
  workers: 2                                                                            
```                                                                                          

Start the server:                                                                       

```                                                                 
llama stack run run.yaml                                                               
```
                                                                                          
Hit the vector store API from two terminals simultaneously:                             

```                                                                                          
# Terminal 1                                                                            
curl -X POST http://localhost:8321/v1/vector_stores \                                   
  -H "Content-Type: application/json" \                                                 
  -d '{"name": "test-store-1", "embedding_model": "all-MiniLM-L6-v2"}'                  
```

```                                                                                          
# Terminal 2 (run at the same time)                                                     
curl -X POST http://localhost:8321/v1/vector_stores \                                   
  -H "Content-Type: application/json" \                                                 
  -d '{"name": "test-store-2", "embedding_model": "all-MiniLM-L6-v2"}'                  
```           
                                                                          

### Error logs

```
sqlite3.OperationalError: database is locked 
```

### Expected behavior

Concurrent writes should wait up to a timeout and succeed, matching the KV store's concurrency behavior. The fix is two lines in _create_sqlite_connection() after sqlite3.connect(db_path):                                                               

```py
connection.execute("PRAGMA journal_mode=WAL")                                           
connection.execute("PRAGMA busy_timeout=5000")                                          
```    
                                                                                   
### Actual Behavior                                                                         
                                                                                          
The second concurrent write fails immediately with no retry because the default         
SQLite journal mode (DELETE) uses exclusive locks and no busy_timeout is set.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9ed901b21d03bbe90cf75996679a6a6757ddb3ba`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "ogx_ai_ogx__5344__9ed901b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
