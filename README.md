Here is my solution to the fetch.

##
Docker Set up

1. Build the docker contianer with :

  docker build -t receipt-processor . 
  
2.Run the container with: 

 docker run -p 8000:8000 receipt-processor


 Then you could run my test to make sure it works or use postman as well to verify.
 Or you could call a curl command to test. Really whatever you decide
