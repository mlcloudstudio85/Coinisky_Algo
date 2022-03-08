# sql-net
Getting Data:

  https://drive.google.com/drive/folders/1qhcGbrZO0Qve5b9Q1tvoP4FmFUum1a1q?usp=sharing
  
Data path:
  ./Sqlnet/data
  
Getting glove embedding:
  bash download_glove.sh
  
 To RUN:
 
 Step 1: Set up poetry virtual env
 
         command:
         poetry init
         poetry shell
         poetry update
      
 Step 2: preprocessing of glove embedding
 
        python extract_vocab.py
       
 step 3: to train model
 
      python train.py -h     
 train model with column attention(optional)
 
      python train.py --ca
      
  step 4: to test
  
      python test.py --ca
