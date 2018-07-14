# Code-samples for using gcloud and Python Client Library for Google Compute Engine

This repository contains some examples of using gcloud with shell scripts and python scripts and also using the Python Client Library APIs to perform some basic automation. 

Refer to https://medium.com/google-cloud/using-gcloud-to-get-google-cloud-platform-data-you-need-c4985b416278 for more details

## Prerequisites

The scripts work when tested using the Google cloud shell. This is not tested with SDK on the personal computer, but it should work. Check https://cloud.google.com/sdk/install if you want to try it out.

## Few points about the environment/setup used in the examples

The examples here will probably not work in your environment as-is. For example, the label key and values used here should be changed as per your labeling strategy. My advice would be to read and understand the code first and then modify it to fit your environment.

## Contributing

Please feel free to try the code and add/suggest new functionality and approaches. Please leave a comment here or on the Medium post.

## Authors

* **Shashank Joshi** https://github.com/shashyajoshi/

## Disclaimer and other important comments

* Completeness - The scripts here are provided to serve as an example of using gcloud and the Python Client Library. They are in no way complete solutions in themselves.
* Coding best practices - In real-world deployment you should think about coding best practices, such as, error checking/handling, functionality to check and wait for actions to complete, log/print meaningful messages and so on

## License

See the [LICENSE.md](LICENSE.md) file for details
