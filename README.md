# Daily Paper Recommendation

I normally sort arxiv by new and select papers of interest to read every day. I'm hoping to incorporate more ML / DL into this process. 

Currently, the process involves:

1. Hitting the ARXIV API for the most recent papers (will be designed to run each day)
2. Embed a selected historical list of paper titles
3. Compute cosine similarity to embeddings of paper titles from today
4. Return the most similar papers

Some further to dos:

1. Deploy as an app to be called
2. Change into a knowledge graph
3. Evaluate feasibility of considering abstract as well
4. Automatically hit Mendeley API to retrieve titles list (for some reason, can't get access token ATM)