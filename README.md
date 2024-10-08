# Fetch all forks of a repo on Github by Org

This is to fetch all forks of a repo on Github that are forked by orgs instead of individuals

## Steps

1. Create a virtual environment

```
python3 -m venv myenv
```

2. Activate the virtual environment (Need to run this everytime you open a new terminal)

```
source myenv/bin/activate
```

3. Now install deps

```
pip install requests python-dotenv
```

4. Set environment variable

Create a `.env` file in the root of the project and add the following

```
GITHUB_TOKEN=<your_github_token>
```

5. Run the script

```
python main.py
```
