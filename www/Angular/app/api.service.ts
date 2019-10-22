import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class ApiService {
  API_URL = 'http://localhost:8000';

  public login_username;
  public login_email;

  public username;
  public Email;

  constructor(private httpClient: HttpClient, private router: Router) { }

  generateToken(userData){
  return this.httpClient.post(`${this.API_URL}/api/v1/rest-auth/login/`, userData);
  
  }

  logout()
      {
        this.router.navigate(['home']);
      }
}
