class ScrollHandler{
	private duration:number;
	private scrolling:boolean;
	private pages:number;
		
	constructor(containerId:string,duration:number =500){
		this.pages = document.getElementById(containerId).childElementCount;
		this.scrolling = false;
		this.duration = duration;
		this.hook();
	}
	private getActivePage():number{
		return Math.round(window.pageYOffset/window.innerHeight)+1;
  }
	private setActivePage(pageId:number){
		if(pageId <= this.pages && pageId > 0){
			this.scrolling = true;
			let scrollTo = window.innerHeight * (pageId-1);
			$([document.documentElement, document.body])
				.animate(	{
										scrollTop: scrollTo
									},
									{ 
										duration:	this.duration,
										complete: ()=>{
											this.scrolling = false;
										}
			});
		}
	}
	private hook(){
		window.addEventListener("wheel", (event) => {
				let pageId = this.getActivePage();					
				//Scroll Direction Up : Down
				event.deltaY < 0 ? pageId-- : pageId++;
				//Go
				if(!this.scrolling)	this.setActivePage(pageId);
  	});
	}
}

var myScroll = new ScrollHandler('myScroll');