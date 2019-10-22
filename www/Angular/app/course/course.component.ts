import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent implements OnInit {

  public websocket;


  constructor(public apiservice: ApiService, private http: HttpClient ) { }

  ngOnInit() {
  }

  logout(){
    this.apiservice.logout();
  }

}
