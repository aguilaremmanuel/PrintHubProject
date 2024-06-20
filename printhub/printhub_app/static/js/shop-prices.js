document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-links-container a');
    const currentLink = document.querySelector('.current-link');
    const icons = document.querySelectorAll('.nav-links-container a i');
    const activeIcon = document.querySelector('.active-icon');
    const priceText = document.querySelector('.price-text');
    const linksText = document.querySelectorAll('.nav-links-container a span');

    // Add hover effect to all links except the first one
    for (let i = 0; i < navLinks.length; i++) {

        if(i == 1) {
            continue;
        }else {
            
        }

        navLinks[i].addEventListener('mouseover', function() {
            currentLink.classList.remove('link-hovered');
            navLinks[i].classList.add('link-hovered');
            activeIcon.classList.remove('icon-hovered');
            icons[i].classList.add('icon-hovered');
            priceText.classList.remove('link-text-hovered');
            linksText[i].classList.add('link-text-hovered');
        });
        navLinks[i].addEventListener('mouseout', function() {
            currentLink.classList.add('link-hovered');
            navLinks[i].classList.remove('link-hovered');
            activeIcon.classList.add('icon-hovered');
            icons[i].classList.remove('icon-hovered');
            priceText.classList.add('link-text-hovered');
            linksText[i].classList.remove('link-text-hovered');
        });
    }
});

document.querySelectorAll('.edit-icon').forEach(function(element) {
    element.addEventListener('click', function() {
        const paperType = this.getAttribute('data-id');
        
        document.querySelector('.edit-price-modal').style.display = 'block';
        document.getElementById('paperTypeHidden').value = paperType;
        
        let header = document.getElementById("edit-price-header");

        if(paperType === "short_colored_high") {
            header.textContent = "COLORED (HIGH) - SHORT"
        } else if(paperType === "a4_colored_high") {
            header.textContent = "COLORED (HIGH) - A4"
        } else if(paperType === "long_colored_high") {
            header.textContent = "COLORED (HIGH) - LONG"
        } else if(paperType === "short_colored_medium") {
            header.textContent = "COLORED (MEDIUM) - SHORT"
        } else if(paperType === "a4_colored_medium") {
            header.textContent = "COLORED (MEDIUM) - A4"
        } else if(paperType === "long_colored_medium") {
            header.textContent = "COLORED (MEDIUM) - LONG"
        } else if(paperType === "short_colored_low") {
            header.textContent = "COLORED (LOW) - SHORT"
        } else if(paperType === "a4_colored_low") {
            header.textContent = "COLORED (LOW) - A4"
        } else if(paperType === "long_colored_low") {
            header.textContent = "COLORED (LOW) - LONG"
        } else if(paperType === "short_bw") {
            header.textContent = "BLACK & WHITE - SHORT"
        } else if(paperType === "a4_bw") {
            header.textContent = "BLACK & WHITE - A4"
        } else if(paperType === "long_bw") {
            header.textContent = "BLACK & WHITE - LONG"
        }
        

    });
});

document.getElementById('cancel-edit-price').addEventListener('click', function() {
    document.querySelector('.edit-price-modal').style.display = 'none';
});