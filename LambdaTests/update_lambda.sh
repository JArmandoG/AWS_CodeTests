# Fix for dependencies and custom files of the VENV
PACKAGES='venv/lib/python3.9/site-packages/'
ZIPFILE='new_dependencies.zip'

# Local function to be pushed as a Lambda
LAMBDA_FUNCTION='.py'

# AWS SETTINGS:
# Name of the Lambda to update and its region
MY_LAMBDA=''
REGION=''

zip -r $ZIPFILE .
echo "Zip file updated"
sleep 1

zip -g $ZIPFILE $LAMBDA_FUNCTION
echo "Lambda succesfully zipped"
sleep 1

aws lambda update-function-code --function-name $MY_LAMBDA --zip-file fileb://$ZIPFILE --region $REGION
echo "[!] Lambda is possibly too big to be visualized through the console"
