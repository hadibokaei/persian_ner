# persian_ner

First of all clone the project and go the root of the project directory.

In order to train the model run the following code. It will get the required files except the word embedding which must be manually placed in 'files/'

```angular2html
chmod +x train.sh
./train.sh
```

In order to evaluate the model with the learned model run the following code:

```angular2html
chmod +x evaluate.sh {path to the zip file}
./evaluate.sh
```

In order to use the pretrained models, download them from <a href="https://www.dropbox.com/sh/hagmzbq7nh4vfuj/AACgIuwWUXRT5FChz3RucI_5a?dl=0">this link</a> and place all the files in "files/model/"

