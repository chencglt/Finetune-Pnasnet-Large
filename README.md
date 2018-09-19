# Finetune Pnasnet-Large

This project is based on TF-Slim, and used is for training and testing classifier using PNASNet model.

### Make sure you are running the script of this project under Tensorflow environment.

## Get Start


1. Run the script  "./scripts/download_dataset_checkpoint.sh" in the root directry of this project. It will download the flowers dataset and checkpoint files os PNASNet
2. Start training:

	$ python train_image_classifier.py

3. Evaluate the model:

	$ python eval_image_classifier.py


