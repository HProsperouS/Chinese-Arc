let ProductsInWish = JSON.parse(localStorage.getItem('Wishlist'));


if (!ProductsInWish) {
	ProductsInWish = [];
}



const FavItemNumber = document.querySelector('#total-count')
const parentFavElement = document.querySelector('#WishItems');
const favproducts = document.querySelectorAll('.col-md-3');


const countTotalFavItem = function (){
	let sum = 0
	ProductsInWish.forEach(item => {
		sum += item.count;
	})
	return sum
}

const updateWishListHTML = function () {
	localStorage.setItem('Wishlist', JSON.stringify(ProductsInWish));

	if (ProductsInWish.length > 0) {
		let result = ProductsInWish.map(wishproduct => {
			return `
			
			<li class="buyItem" style='list-style:none;'>
				
			</li>
			<div class="card mb-3" style="max-width: 540px;">
				<div class="row g-0">
					<div class="col-md-4">
						<img src="${wishproduct.image}" class="img-fluid rounded-start" style='margin-left:10px;margin-top:25px;'>
					
					</div>
					<div class="col-md-6">
						<div class="card-body">
							<h5 class="card-title">${wishproduct.name}</h5>
							<div class='badge bg-white' style='font-size:1rem; color:black;'> $ ${wishproduct.price}</div>
							
						</div>
						<div class="row" >
							<i class="btn btn-danger button-delete fas fa-trash-alt" id="remove" value="remove"  style='margin-top:-20px;margin-bottom:20px;margin-left:28px;' onclick="Remove()"> </i>							
						</div>
						
					</div>
					
				</div>
				
			</div>
			`
		});
		parentFavElement.innerHTML = result.join('');
//		document.querySelector('.checkout').classList.add('hidden');

		FavItemNumber.innerHTML = countTotalFavItem();
	}
	else {
		document.querySelector('.checkout').classList.add('hidden');
		parentFavElement.innerHTML = '<h4 class="empty">Oh no! You have not added any favorites yet!</h4>';
		FavItemNumber.innerHTML = ""
	}
}

function Remove(){
	var elem = document.getElementById('remove');
        elem.parentNode.removeChild(elem);
        return false;
}





function updateProductsInWish(wishproduct) { // 2
	document.getElementById('flash_2').textContent = 'Item added to Wishlist!'
		const showFlash = () => {
			flash.classList.add("flash--visible_2")  
			}
		const hideFlash = () => {
			flash.classList.remove("flash--visible_2")
			document.getElementById('flash_2').innerHTML = ''
			}
		// const btn = document.getElementById('checkout')

		showFlash();
		setTimeout(hideFlash, 1000);
		console.log(ProductsInWish)


	for (let i = 0; i < ProductsInWish.length; i++) {
		if (ProductsInWish.id == wishproduct.id) {
            ProductsInWish[i].count += 1;
            ProductsInWish[i].price =  ProductsInWish[i].basePrice *  ProductsInWish[i].count;

			return;
		}
	}
    ProductsInWish.push(wishproduct);
	
}
favproducts.forEach(item => {   // 1

	item.addEventListener('click', (e) => {

		if (e.target.classList.contains('addToWish')) {
			const productID = e.target.dataset.productId;
			const productName = item.querySelector('.productName').innerHTML;
			const productPrice = item.querySelector('.priceValue').innerHTML;
			const productImage = item.querySelector('img').src;
			let wishproduct = {
				name: productName,
				image: productImage,
				id: productID,
				count:1,
				price: +productPrice,
				basePrice: +productPrice,
			}
			
			updateProductsInWish(wishproduct);
			updateWishListHTML();

			
		}
	

	});

});

parentFavElement.addEventListener('click', (e) => { // Last
	const isPlusButton = e.target.classList.contains('button-plus');
	const isMinusButton = e.target.classList.contains('button-minus');
	const isDeleteButton = e.target.classList.contains('button-delete');
	
	if (isPlusButton || isMinusButton || isDeleteButton) {
		
		for (let i = 0; i < ProductsInWish.length; i++) {
			if (ProductsInWish[i].id == e.target.dataset.id) {
				if (isPlusButton) {
					ProductsInWish[i].count += 1

				}
				else if (isMinusButton) {
					ProductsInWish[i].count -= 1
				}
				else if (isDeleteButton){
					ProductsInWish[i].count = 0

					ProductsInWish[i].price = ProductsInWish[i].basePrice * ProductsInWish[i].count;

				

				}
				

			}
			if (ProductsInWish[i].count <= 0) {
				ProductsInWish.splice(i,1); //The splice() method adds and/or removes array elements
			}
		} 
		updateWishListHTML();
	} 
});

updateWishListHTML();
function Delete(){
	
}





