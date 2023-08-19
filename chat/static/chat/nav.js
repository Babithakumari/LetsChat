document.addEventListener('DOMContentLoaded',function(){
    
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");

hamburger.addEventListener("click", mobileMenu);

const navLink = document.querySelectorAll(".nav-link");
navLink.forEach(n => n.addEventListener("click", closeMenu));


// To enable search bar
searchForm = document.querySelector("#search-form")

if(searchForm){
    searchForm.onsubmit = () =>{
        person = document.querySelector("#search-bar").value

        searchContact(person)
        return false

    }
}



function mobileMenu() {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
    console.log(navMenu)

}





function closeMenu() {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
}





function searchContact(person)
{

if(person==""){
        location.reload()
}

else{
    fetch(`search_contact/${person}`)
    .then(response => response.json())
    .then(data =>
        {
            if (data.status == "failure")
            {
                window.location.href="http://127.0.0.1:8000/chat/error"
            }
            
           
            else if (data.status == "success")
            {
                window.location.href="http://127.0.0.1:8000/chat/found/"+ `${person}`

            }
            
            else if (data.status == "pending")
            {
                fetch(`create_contact/${person}`)
                .then(response => response.json())
                .then(data =>
                    {
                        window.location.href="http://127.0.0.1:8000/chat/found/"+ `${person}`

                        

                    })
            }
            

            
        })


            
        
    }
document.querySelector('#search-bar').value=""

}})







