console.log("Account Js is working")

$("#profileImage").click(function(e) {
    $("#uploadImage").click();
});

function fasterPreview( uploader ) {
    if ( uploader.files && uploader.files[0] ){
          $('#profileImage').attr('src', 
             window.URL.createObjectURL(uploader.files[0]) );
    }
}

$("#uploadImage").change(function(){
    fasterPreview( this );
});