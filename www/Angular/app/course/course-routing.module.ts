import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CourseComponent} from './course.component';
import { TopicChatComponent} from './topic-chat.component';
import { TopicVideosComponent } from './topic-videos.component';
import { TopicLabsComponent } from './topic-labs.component';


const courseRoutes: Routes = [

  
    {
      path: 'course',
      component: CourseComponent,
      
      children: [
        {
          path: '',
          
          children: [
            { path: 'topic-videos', component: TopicVideosComponent },
            { path: 'topic-labs', component: TopicLabsComponent },
            { path: 'topic-chat', component: TopicChatComponent }
          ]
        }
      ]
    }
  ];
@NgModule({
  imports: [RouterModule.forChild(courseRoutes)],
  exports: [RouterModule]
})
export class CourseRoutingModule { }
