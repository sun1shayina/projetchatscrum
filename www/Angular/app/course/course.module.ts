import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CourseComponent } from './course.component';
import { TopicVideosComponent } from './topic-videos.component';
import { TopicLabsComponent } from './topic-labs.component';
import { TopicChatComponent } from './topic-chat.component';
import { CourseRoutingModule } from './course-routing.module';


@NgModule({
  imports: [
    CommonModule,
    CourseRoutingModule
    
  ],
  declarations: [
    CourseComponent,
    TopicVideosComponent,
    TopicLabsComponent,
    TopicChatComponent
    
  ],
  providers: [],
  bootstrap: [CourseComponent]
})
export class CourseModule { }
