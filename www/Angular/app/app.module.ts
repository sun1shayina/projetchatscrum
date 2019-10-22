import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { DataService } from './data.service';
import { FormsModule } from '@angular/forms';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { UserComponent } from './user/user.component';

import { GenerateTokenComponent } from './generate-token/generate-token.component';
import { GroupClassComponent } from './group-class/group-class.component';
import { SignupComponent } from './signup/signup.component';

import { HttpClientModule } from '@angular/common/http';
import { ProfileComponent } from './profile/profile.component';

import { DragulaModule } from 'ng2-dragula';
import { MzButtonModule, MzModalModule } from 'ngx-materialize';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    UserComponent,
    ProfileComponent,
    GenerateTokenComponent,
    GroupClassComponent,
    SignupComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    MzButtonModule,
    MzModalModule,
    DragulaModule.forRoot()
  ],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
