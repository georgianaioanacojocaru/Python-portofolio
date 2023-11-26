document.addEventListener("DOMContentLoaded", function () {
    var profilePicInput = document.getElementById("profile_pic");

    profilePicInput.addEventListener("change", function () {
        var profilePicDiv = document.querySelector(".profile_pic");
        var file = profilePicInput.files[0];

        if (file) {
            var reader = new FileReader();

            reader.onload = function (e) {
                profilePicDiv.style.backgroundImage = "url('" + e.target.result + "')";
            };

            reader.readAsDataURL(file);
        }
    });
});