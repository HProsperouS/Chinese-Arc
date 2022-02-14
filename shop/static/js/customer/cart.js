let productsInCart = JSON.parse(localStorage.getItem('shoppingCart'));

if(!productsInCart){
	productsInCart = [];
}
// const parentElement = document.querySelector('#buyItems');
// const cartSumPrice = document.querySelector('#sum-prices');
// const products = document.querySelectorAll('.product-under');
// const cartItemNumber= document.querySelector('#sum-count');

const parentElement = document.querySelector('#buyItems');
const cartSumPrice = document.querySelector('#sum-price');
const products = document.querySelectorAll('.col-md-3');
const cartItemNumber= document.querySelector('#sum-count');
const flash_2 = document.getElementById('flash_2')
const flash = document.getElementById('flash')

// const CartCallout = function(){
//   alert("Item added to cart!");
// }

const countTheSumPrice = function () { // 4
	let sum = 0;
	productsInCart.forEach(item => {
		sum += item.price;
	});
	return sum;
}

const countTotalItem = function (){
	let sum = 0
	productsInCart.forEach(item => {
		sum += item.count;
	})
	return sum
}

const updateShoppingCartHTML = function () {  // 3
	localStorage.setItem('shoppingCart', JSON.stringify(productsInCart));
	if (productsInCart.length > 0) {
		let result = productsInCart.map(product => {
			return `
			<li class="buyItem" style='list-style:none;'>
				
			</li>
			<div class="card mb-3" style="max-width: 540px;">
				<div class="row g-0">
					<div class="col-md-4">
						<img src="${product.image}" class="img-fluid rounded-start" style='margin-left:10px;margin-top:25px;'>
					
					</div>
					<div class="col-md-6">
						<div class="card-body">
							<h5 class="card-title">${product.name}</h5>
							<div class='qnty'>
								<i class="fas fa-minus button-minus mr-1" data-id=${product.id} type='button'></i>
						
								<span class="countOfProduct">${product.count}</span>
								
								<i class="fas fa-plus button-plus ml-1" data-id=${product.id} type='button'></i>
								
										
							</div>
							<div class='badge bg-secondary' style='font-size:1rem;'> $ ${product.price}</div>
							
						</div>
						<div class="row" >
							<i class="btn btn-danger button-delete fas fa-trash-alt"  data-id=${product.id} style='margin-top:-20px;margin-bottom:20px;margin-left:28px;'> </i>
						</div>
						
					</div>
					
				</div>
				
			</div>
			`
			
		});
		parentElement.innerHTML = result.join('');
		
		document.querySelector('.checkout').classList.remove('hidden');

		cartItemNumber.innerHTML = countTotalItem() ;

	}
	else {
		document.querySelector('.checkout').classList.add('hidden');
		parentElement.innerHTML = '<h4 class="empty text-center">Your shopping cart is empty!</h4> ';
		cartSumPrice.innerHTML = '';
		cartItemNumber.innerHTML = '';


	}
}

function updateProductsInCart(product) { // 2
	document.getElementById('flash_2').textContent = 'Item added to Cart!'
		const showFlash = () => {
			flash_2.classList.add("flash--visible_2")  
			}
		const hideFlash = () => {
			flash_2.classList.remove("flash--visible_2")
			document.getElementById('flash_2').innerHTML = ''
			}
		// const btn = document.getElementById('checkout')

		showFlash();
		setTimeout(hideFlash, 1000);


	for (let i = 0; i < productsInCart.length; i++) {
		if (productsInCart[i].id == product.id) {
			productsInCart[i].count += 1;
			productsInCart[i].price = productsInCart[i].basePrice * productsInCart[i].count;

			return;
		}
	}

	productsInCart.push(product);
	
}

products.forEach(item => {   // 1

	item.addEventListener('click', (e) => {

		if (e.target.classList.contains('addToCart')) {
			const productID = e.target.dataset.productId;
			const productName = item.querySelector('.productName').innerHTML;
			const productPrice = item.querySelector('.priceValue').innerHTML;
			const productImage = item.querySelector('img').src;
		
			let product = {
				name: productName,
				image: productImage,
				id: productID,
				count:1,
				price: +productPrice,
				basePrice: +productPrice,
			}

			updateProductsInCart(product);
			updateShoppingCartHTML();
			AddtoCart(product);
			
			
		}
		// alert("Item added to cart!"); // Pop up when click on add to cart

	});

});

parentElement.addEventListener('click', (e) => { // Last
	const isPlusButton = e.target.classList.contains('button-plus');
	const isMinusButton = e.target.classList.contains('button-minus');
	const isDeleteButton = e.target.classList.contains('button-delete');
	
	if (isPlusButton || isMinusButton || isDeleteButton) {
		
		for (let i = 0; i < productsInCart.length; i++) {
			if (productsInCart[i].id == e.target.dataset.id) {
				if (isPlusButton) {
					productsInCart[i].count += 1

					AddtoCart(productsInCart[i])
				}
				else if (isMinusButton) {
					productsInCart[i].count -= 1

					MinusCart(productsInCart[i])
				}
				else if (isDeleteButton){
				productsInCart[i].count = 0

				productsInCart[i].price = productsInCart[i].basePrice * productsInCart[i].count;

				Deleteitem(productsInCart[i])
				

				}
				

			}
			if (productsInCart[i].count <= 0) {
				productsInCart.splice(i,1); //The splice() method adds and/or removes array elements
			}
		}
		updateShoppingCartHTML();
		

	}
	
});

updateShoppingCartHTML();

function AddtoCart(product){
	console.log('add')
	for (let i = 0; i < productsInCart.length; i++) {
		if (productsInCart[i].id == product.id) {
			if (productsInCart[i].count > 1) {
				fetch('/createCustOrder',{
					method:'POST',
					body: JSON.stringify({
						function:'plus',product_name : product.name, product_price: product.price, product_qty : product.count
					}),
					cache: 'no-cache',
					headers: new Headers({
						'content-type': 'application/json'
					})
				})
				
			}
			else if (productsInCart[i].count == 1){
				fetch('/createCustOrder',{
					method:'POST',
					body: JSON.stringify({
						function:'add',product_name : product.name, product_price: product.price, product_qty : product.count
					}),
					cache: 'no-cache',
					headers: new Headers({
						'content-type': 'application/json'
					})
				})
				
			}
		}
	}
}

function MinusCart(productsInCart){
	fetch('/createCustOrder',{
		method:'POST',
		body: JSON.stringify({
			function:'minus',product_name : productsInCart.name, product_price: productsInCart.price, product_qty : productsInCart.count
		}),
		cache: 'no-cache',
		headers: new Headers({
			'content-type': 'application/json'
		})
	})

}

function Deleteitem(productsInCart){
	fetch('/createCustOrder',{
		method:'POST',
		body: JSON.stringify({
			function:'delete',product_name :productsInCart.name, product_price: productsInCart.price, product_qty : productsInCart.count
		}),
		cache: 'no-cache',
		headers: new Headers({
			'content-type': 'application/json'
		})
	
	})
}

// // cartSumPrice.innerHTML = '$' + countTheSumPrice();
// let count_1 = 0;
// //if add to cart btn clicked
// $('.addToCart').on('click', function (){
// let cart = $('.openbtn');
// // find the img of that card which button is clicked by user
// let imgtodrag = find("img").eq(0);
// if (imgtodrag) {
// 	// duplicate the img
// 	var imgclone = imgtodrag.clone().offset({
// 	top: imgtodrag.offset().top,
// 	left: imgtodrag.offset().left
// 	}).css({
// 	'opacity': '0.8',
// 	'position': 'absolute',
// 	'height': '150px',
// 	'width': '150px',
// 	'z-index': '100'
// 	}).appendTo($('body')).animate({
// 	'top': cart.offset().top + 20,
// 	'left': cart.offset().left + 30,
// 	'width': 75,
// 	'height': 75
// 	}, 1000, 'easeInOutExpo');

// 	// setTimeout(function(){
// 	// count++;
// 	// $(".cart-nav .item-count").text(count_2);
// 	// }, 1500);

// 	imgclone.animate({
// 	'width': 0,
// 	'height': 0
// 	}, function(){
// 	$(this).detach()
// 	});
// }
// });

