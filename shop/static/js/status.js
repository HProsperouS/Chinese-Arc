
window.onload = () => {
    var order_id = document.getElementById('order_id').textContent
    
    
    
    if (document.getElementById('Status').textContent == 'Delivered') {
        document.getElementById('Status').classList = 'badge bg-success'
        // badge.classList.remove('bg-secondary')
        // badge.classList.add('bg-success')
    }
    else if (document.getElementById('Status').textContent == 'Pending'){
        document.getElementById('Status').classList = 'badge bg-secondary'
        // badge.classList.remove('bg-success')
        // badge.classList.add('bg-secondary')
    }
    else if (document.getElementById('Status').textContent == 'Undelivered'){
        document.getElementById('Status').classList = 'badge bg-danger'
    }
    
}
// function Status(){
//     var order_id = document.getElementById('order_id').textContent
//     console.log(order_id)
//     if (document.getElementById('Status').textContent == 'Delivered') {
//         document.getElementById('Status').classList = 'badge bg-success'
//         // badge.classList.remove('bg-secondary')
//         // badge.classList.add('bg-success')
//     }
//     else if (document.getElementById('Status').textContent == 'Pending'){
//         document.getElementById('Status').classList = 'badge bg-secondary'
//         // badge.classList.remove('bg-success')
//         // badge.classList.add('bg-secondary')
//     }
//     else if (document.getElementById('Status').textContent == 'Undelivered'){
//         document.getElementById('Status').classList = 'badge bg-danger'
//     }
    
// }