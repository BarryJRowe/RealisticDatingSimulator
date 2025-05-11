# Realistic Dating Simulator

To run:
```
pip install -r requirements.txt
python3 serve.py
```

`config.json` options:

```
{
 "groq_key": "...", 
 "port": 4000, 
 "local_llm": false, 
 "difficulty": 1.4
}
```

Using a `groq` key is recommend for a faster experience. However, for free usage, you can set `local_llm` to be `true`, which will download an llm model and run it locally, though this will take some time to download and will be a slower experience.


Once `serve.py` is running, go to: `http://localhost:4000/` to start playing. 
