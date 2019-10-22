import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-generate-token',
  templateUrl: './generate-token.component.html',
  styleUrls: ['./generate-token.component.css']
})
export class GenerateTokenComponent implements OnInit {

  constructor(private apiService: ApiService, private router: Router) { }
  
  register;

  ngOnInit() {
    this.register = {
      username: '',
      password: '',
      email: ''
    }
  }

  generateToken(){
    this.apiService.generateToken(this.register).subscribe(response => {
        console.log(response);
        this.router.navigate(['course'])
      },
      error => window.alert("Invalid Credentials")
      );
      };

     logout()
      {
        
        this.router.navigate(['home']);
      }

}
