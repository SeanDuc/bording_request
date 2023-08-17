# this is bored :)

## requirments

this project requires pipenv, which can be installed using `pip install pipenv`.

## setup

```
pipenv install
pipenv shell
```

make sure to have your OWN openai key generated and attached to an account.
to insert your oun key do the following:

1. locate the file in the route directory of this project called "._env"
2. rename the file ".env" by removing the "_"
3. edit the file and replace "Replace With OpenAI Key" with your openAI key
4. save and close

## run

in order to run type the following:
```
uvicorn main:app --reload
```