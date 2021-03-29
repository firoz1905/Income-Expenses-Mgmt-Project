from django.contrib.auth.tokens import  PasswordResetTokenGenerator ### we are going to use this here for user activation purposes
from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):
    ## This PasswordResetTokenGenerator built into django for securely managing intricacies of users password which is making sure that user not able to reuse the samelink to reset the password.
    def _make_hash_value(self,user,timestamp): ## when creating the token this method will run
        ## text_type will make sure what we are sending is compatable with the systems it is going to ineracting
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))

token_generator= AppTokenGenerator() ## instantiating our class