const voucher_1 = document.getElementById("voucher_1")
function openlist() { 
    // document.getElementById("voucherlist hide").style.height= "300px";
    voucher_1.classList.add('show')
    document.getElementById("close-button").classList.remove('hide')
    // document.querySelector(".listpanel").style.display= 'block';
    // document.getElementById("voucherlist hide").classList.add = 'show';
    // document.getElementById("overlay").style.display = "block";
}


function closelist() {
    document.getElementById("voucherlist hide").style.height = "0";
    voucher_1.classList.remove('show')
    document.getElementById("close-button").classList.add('hide')

    // document.getElementById("overlay").style.display = "none";
}
