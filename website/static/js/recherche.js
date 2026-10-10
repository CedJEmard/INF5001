const reponse = document.getElementById("reponse");
const searchbar = document.getElementById("sans-resultat");


function myFunction() {
    if (reponse.style.display === "block") {
        reponse.style.display = "none";
    } else {
        reponse.style.display = "block";
    }

    if (document.getElementById("sans-resultat")) {
        searchbar.id = "top";
        document.getElementById("bouton-test").style.backgroundColor = 'green'; /* TODO delete button */
    } else if (document.getElementById("top")) {
        document.getElementById("top").id = "sans-resultat";
        document.getElementById("bouton-test").style.backgroundColor = 'red'; /* TODO delete button */
    }


}