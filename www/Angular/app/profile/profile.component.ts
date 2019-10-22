import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { DragulaService } from 'ng2-dragula';
import { Subscription, Observable } from 'rxjs';
import { forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MzModalModule } from 'ngx-materialize';
@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  public arrCount = [0, 1, 2, 3];
  subs = new Subscription();
  public show_zero: boolean = true;
  public show_history: boolean = false;
  public show_project_chat: boolean = false;
  public show_sprint_option: boolean = false;
  public chat_text: string = "";
  public messages = [];
  public websocket;
  public msg_obs;
  public on_user;
  public at_bottom: boolean = true;
  public id_hover = -1;
  public id_click = -1;
  sprint_start: Number;
  sprint_end: Number;
  goal_id: string;
  public chat_div_title: string = "Project Chat"
  present_scrum;
   public task_history: any;
  public iData: any;
  public image_upload: File = null;
  public scrum_image: File = null;
  public selected_history:any = [];
    
  public modalOptions: Materialize.ModalOptions = {
    dismissible: false, // Modal can be dismissed by clicking outside of the modal
    opacity: .5, // Opacity of modal background
    inDuration: 300, // Transition in duration
    outDuration: 200, // Transition out duration
    startingTop: '100%', // Starting top style attribute
    endingTop: '10%', // Ending top style attribute
    ready: (modal, trigger) => { // Callback for Modal open. Modal and trigger parameters available.
      alert('Ready');
      console.log(modal, trigger);
    },
    complete: () => { alert('Closed'); } // Callback for Modal close
  };
  
  constructor(
      public dataservice: DataService, private dragula: DragulaService, private http: HttpClient, private modalModule: MzModalModule
      ) { 
    this.dragula.createGroup('mainTable', {
        revertOnSpill: true,
        direction: 'horizontal',
        invalid: (el) => {
            return el.id == 'author' || el.id == 'remove' || el.id == 'blank';
        }
    });
    
    this.subs.add(
        this.dragula.drop('mainTable').subscribe(
            value => {
                console.log(value);
                var el = value['el'];
                var target = value['target'];
                var source = value['source'];
                
                if (target['parentElement'] == source['parentElement']) {
                    var hours = -1;
                    if(target['id'] == '2' && source['id'] == '1')
                    {
                        var hours_in = window.prompt('How many hours did you spend on this task?');
                        hours = parseInt(hours_in, 10);
                        if(hours + '' == 'NaN')
                            hours = -1;
                    }
                    this.dataservice.moveGoal(el['id'], target['id'], hours);
                if (this.dataservice.selected_sprint) {
                  this.changeSprint()
                }
                else{
                  this.filterSprint(this.dataservice.sprints)
                }
                } else {
                    this.dataservice.changeOwner(el['id'], target['parentElement']['id']);
                } 
            }
        )
    );
    
    this.dataservice.realname = sessionStorage.getItem('realname');
    this.dataservice.username = sessionStorage.getItem('username');
    this.dataservice.role = sessionStorage.getItem('role');
    this.dataservice.project = sessionStorage.getItem('project_id');

    this.dataservice.authOptions = {
        headers: new HttpHeaders({'Content-Type': 'application/json', 'Authorization': 'JWT ' + sessionStorage.getItem('token')})
    };
    this.dataservice.imageAuthOptions = {
        headers: new HttpHeaders({'Authorization': 'JWT ' + sessionStorage.getItem('token')})
    };
    this.msg_obs = new MutationObserver((mutations) => {
        var chat_scroll = document.getElementById('chat_div_space');
        console.log(chat_scroll.scrollHeight - chat_scroll.clientHeight);
        console.log(chat_scroll.scrollTop);
        if(this.at_bottom)
            chat_scroll.scrollTop = chat_scroll.scrollHeight - chat_scroll.clientHeight;
        console.log(this.messages);
    });

    this.websocket = new WebSocket('ws://' + this.dataservice.domain_name + '/scrum/');
    this.websocket.onopen = (evt) => {
      forkJoin(
          this.http.get('http://' + this.dataservice.domain_name + '/scrum/api/scrumprojects/' + this.dataservice.project + '/', this.dataservice.httpOptions),
          this.http.get('http://' + this.dataservice.domain_name + '/scrum/api/scrumsprint/?goal_project_id=' + this.dataservice.project, this.dataservice.authOptions)
        )
         .subscribe(([res1, res2]) => {
            this.msg_obs.observe(document.getElementById('chat_div_space'), { attributes: true, childList: true, subtree: true });
            this.dataservice.users = res1['data'];
            this.dataservice.project_name = res1['project_name'];
            this.dataservice.sprints = res2;
            this.websocket.send(JSON.stringify({'user': this.dataservice.realname, 'message': '!join ' + this.dataservice.project_name, 'goal_id': 'main_chat_' + this.dataservice.project_name }));
            console.log(this.dataservice.users)


            this.filterSprint(res2)
        },
        err => {
                this.dataservice.message = 'Unexpected Error!';
                console.log(err);
            });

    }

    this.websocket.onmessage = (evt) => {
        var data = JSON.parse(evt.data);
        if(data['messages'] !== undefined)
        {
            this.messages = []
            for(var i = 0; i < data['messages']['length']; i++)
            {
                this.messages.push(data['messages'][i]['user'] + ': ' + data['messages'][i]['message']);
            }
        } else
        {
            this.messages.push(data['user'] + ': ' + data['message']);
        }
        this.at_bottom = false;
        var chat_scroll = document.getElementById('chat_div_space');
        if(chat_scroll.scrollTop == chat_scroll.scrollHeight - chat_scroll.clientHeight)
            this.at_bottom = true;
    }

    this.websocket.onclose = (evt) => {
        console.log('Disconnected!');
        this.msg_obs.disconnect();
    }
  }
  

  swapState()
  {
    this.show_zero = !this.show_zero;  
  }


  changeSprint() 
  {   
    this.dataservice.sprint_goals = [];
      for (var i = 0;  i < this.dataservice.users.length; i++)  {
        for (var j = 0;  j < this.dataservice.users[i].scrumgoal_set.length; j++)  {
          if (this.dataservice.users[i].scrumgoal_set[j].time_created > this.dataservice.selected_sprint.created_on && 
            this.dataservice.users[i].scrumgoal_set[j].time_created < this.dataservice.selected_sprint.ends_on)
            {                
             this.dataservice.users[i].scrumgoal_set[j].user_id = this.dataservice.users[i].id;
             this.dataservice.sprint_goals.push(this.dataservice.users[i].scrumgoal_set[j]);
            }
          } 
        }
  }

            
  filterSprint(uSprints) {
    this.dataservice.sprints= uSprints
    var filter_goal = []
    console.log(filter_goal)
        // this.dataservice.sprint_goals.length = 0 
          for (var i = 0;  i < this.dataservice.users.length; i++)  {
            for (var j = 0;  j < this.dataservice.users[i].scrumgoal_set.length; j++)  {
              if (this.dataservice.sprints.length) {
                if (this.dataservice.users[i].scrumgoal_set[j].time_created >= this.dataservice.sprints[this.dataservice.sprints.length - 1].created_on && 
                  this.dataservice.users[i].scrumgoal_set[j].time_created <= this.dataservice.sprints[this.dataservice.sprints.length - 1].ends_on)
                  {                  
                  // console.log(this.dataservice.users[i].scrumgoal_set[j].time_created)
                  // console.log(this.dataservice.users[i].scrumgoal_set[j].name)
                   // this.dataservice.users[i].scrumgoal_set[j].user_id = this.dataservice.users[i].id
                   filter_goal.push(this.dataservice.users[i].scrumgoal_set[j]);
                   
                  }this.show_sprint_option = true;
              } else {
                  this.dataservice.users[i].scrumgoal_set[j].user_id = this.dataservice.users[i].id
                  filter_goal.push(this.dataservice.users[i].scrumgoal_set[j]); 
                  
              }
            }
          }
          // console.log(filter_goal)
          this.dataservice.sprint_goals = filter_goal

  }


  createSprintMethod(myDate) {
          console.log(this.dataservice.users)
          console.log(this.dataservice.sprints)
          forkJoin(
          this.http.post('http://' + this.dataservice.domain_name + '/scrum/api/scrumsprint/?goal_project_id=' + this.dataservice.project, JSON.stringify({'project_id': this.dataservice.project, 'ends_on': myDate}), this.dataservice.authOptions),
          this.http.get('http://' + this.dataservice.domain_name + '/scrum/api/scrumprojects/' + this.dataservice.project + '/', this.dataservice.httpOptions)
        )
         .subscribe(([res2, res1]) => {
            this.msg_obs.observe(document.getElementById('chat_div_space'), { attributes: true, childList: true, subtree: true });
            this.dataservice.users = res2['users'];
            this.dataservice.project_name = res1['project_name'];
            this.dataservice.sprints = res2['data']
            this.dataservice.message = res2['message']
            
            console.log(this.dataservice.sprints)
            console.log(this.dataservice.users)
            console.log(this.dataservice.sprint_goals)
            this.filterSprint(res2['data'])
            console.log(this.dataservice.sprint_goals)
        },

            err => {
              console.error(err);
                if(err['status'] == 401)
                  {
                    this.dataservice.message = 'Session Invalid or Expired. Please Login.';
                    this.dataservice.logout();
                } else
                  {
                    this.dataservice.message = 'Unexpected Error!';    
                  }
                }
              );
  }

  createSprint() 
  {
    var myDate = new Date(new Date().getTime()+(7*24*60*60*1000));
    if (this.dataservice.sprints.length) {
      console.log('if works');
      var present_scrum_id = this.dataservice.sprints[this.dataservice.sprints.length - 1].id;
      this.present_scrum = this.dataservice.sprints[this.dataservice.sprints.length - 1].ends_on;
      this.present_scrum =  new Date(this.present_scrum).valueOf();
      
      
      //  Test if Today Date is greater than last scrum
      console.log(this.present_scrum);
      console.log(new Date().valueOf());
      if (this.present_scrum > new Date().valueOf()) {
        if (confirm("Sprint #" + present_scrum_id + " is currently running. End this spring and start another one?  Click \"OK\" to continue Create New Sprint!!!")) {
          this.dataservice.message == "Current Sprint ended";          
          this.createSprintMethod(myDate)
          return;
            }
        else {
          this.dataservice.message = 'Last Sprint continued!!!';
          console.log("Sprint Continue");
          return;
            
        }
      } else  {
          this.createSprintMethod(myDate);
        
          return;
      }   
    } else {
        console.log('else works');
        this.createSprintMethod(myDate);
        
        return;
    }    
  } 

  
  editGoal(event)
  {
    console.log(this.dataservice.selected_sprint);
    console.log(this.dataservice.users);
    var taskID = event.target.parentElement.id.substring(1);
    var message = null;
    for(var i = 0; i < this.dataservice.users.length; i++)
    {
        if(this.dataservice.users[i].id == event.target.parentElement.parentElement.parentElement.id.substring(1))
        {
            for(var j = 0; j < this.dataservice.users[i].scrumgoal_set.length; j++)
            {
                if(this.dataservice.users[i].scrumgoal_set[j].goal_project_id == taskID)
                {
                    message = this.dataservice.users[i].scrumgoal_set[j].name;
                    break;
                }
            }
            break;
        }
    }
    var goal_name = window.prompt('Editing Task ID #' + taskID + ':', message);
    if(goal_name == null || goal_name == '')
    {
        this.dataservice.message = 'Edit Canceled.';
    } else
    {
        this.http.put('http://' + this.dataservice.domain_name + '/scrum/api/scrumgoals/', JSON.stringify({'mode': 1, 'goal_id': event.target.parentElement.id, 'new_name': goal_name, 'project_id': this.dataservice.project}), this.dataservice.authOptions).subscribe(
            data => {
                this.dataservice.users = data['data'];
                this.dataservice.message = data['message'];                
                if (this.dataservice.selected_sprint) {
                  this.changeSprint()
                }
                else{
                  this.filterSprint(this.dataservice.sprints)
                }
            },
            err => {
                console.error(err);
                if(err['status'] == 401)
                {
                    this.dataservice.message = 'Session Invalid or Expired. Please Login.';
                    this.dataservice.logout();
                } else
                {
                    this.dataservice.message = 'Unexpected Error!';    
                }
            }
        );
    }
  }

  deleteTask(goal_name, goal_id) {
      var pop_event = window.confirm('Delete " ' + goal_name + '"?');
      console.log(goal_id)
      if (pop_event) {
          this.http.put('http://' + this.dataservice.domain_name + '/scrum/api/scrumgoals/', JSON.stringify({'mode': 2, 'goal_id':'g' + goal_id, 'new_name': goal_name, 'project_id': this.dataservice.project}), this.dataservice.authOptions).subscribe(
            data => {
                this.dataservice.users = data['data'];
                this.dataservice.message = data['message'];
                if (this.dataservice.selected_sprint) {
                  this.changeSprint()
                }
                else{
                  this.filterSprint(this.dataservice.sprints)
                }
                
                
            },
            err => {
                console.error(err);
                if(err['status'] == 401)
                {
                    this.dataservice.message = 'Session Invalid or Expired. Please Login.';
                    this.dataservice.logout();
                } else
                {
                    this.dataservice.message = 'Unexpected Error!';    
                }
            }
        );
      } else {
          console.log('cancel');
      };
    }
  
  manageUser(event)
  {
    this.getClicked(event);
    var role_name = window.prompt('Change User Role:\nSelect Between: Developer, Admin, Quality Analyst, or Owner:', '');
    if(role_name == null || role_name == '')
    {
        this.dataservice.message = 'Edit Canceled.';
        return;
    }
    role_name = role_name.toLowerCase();
    if(role_name == 'developer' || role_name == 'quality analyst' || role_name == 'admin' || role_name == 'owner')
    {
        this.http.patch('http://' + this.dataservice.domain_name + '/scrum/api/scrumprojectroles/', JSON.stringify({'role': role_name, 'id': this.on_user, 'project_id': this.dataservice.project}), this.dataservice.authOptions).subscribe(
            data => {
                this.dataservice.users = data['data'];
                this.dataservice.message = data['message'];
            },
            err => {
                console.error(err);
                if(err['status'] == 401)
                {
                    this.dataservice.message = 'Session Invalid or Expired. Please Login.';
                    this.dataservice.logout();
                } else
                {
                    this.dataservice.message = 'Unexpected Error!';    
                }
            }
        );
    } else
    {
        this.dataservice.message = 'Invalid Input.';
    }
  }
  
  doNothing()
  {
     
  }
  
  sendMessage(identity)
  {
    if (this.chat_div_title == "Project Chat") {
      
      this.goal_id = "main_chat_" + this.dataservice.project_name 
      console.log(this.goal_id)
    }
    this.websocket.send(JSON.stringify({'user': this.dataservice.realname, 'message': this.chat_text, 'goal_id': this.goal_id }))
    this.chat_text = '';
  }

  ngOnInit() {

    }

  getClicked(event)
  { 
    console.log()
    if(event.target.parentElement.parentElement.parentElement.parentElement.id) {
        this.on_user = event.target.parentElement.parentElement.parentElement.parentElement.id;
      console.log(this.on_user)
    } else {
    this.on_user = event.target.parentElement.parentElement.parentElement.parentElement.parentElement.id 
    console.log(this.on_user)
  }
  }

  goalClicked(clicked_goal_id) { 
      console.log(clicked_goal_id);
      this.goal_id = "G" + clicked_goal_id;
    }

  initGoalChat(){
    this.websocket.send(JSON.stringify({'user': this.dataservice.realname, 'message': '!goal_chat' + this.goal_id, 'goal_id': this.goal_id }))
    this.show_project_chat = true;
    this.chat_div_title = this.goal_id + " Chat"
  }

  initMainChat(){
    this.websocket.send(JSON.stringify({'user': this.dataservice.realname, 'message': '!join ' + this.dataservice.project_name, 'goal_id': 'main_chat_' + this.dataservice.project_name }));
    this.chat_div_title = "Project Chat"
  }


  // imageUpload()  {
  //   console.log(this.dataservice.authOptions)
  //   console.log(this.image_upload)
  //   let details = {
  //       'mode': 1,
  //       'goal_id': this.goal_id, 
  //       'project_id': this.dataservice.project,
  //       // 'file':this.image_upload
  //     };
  //   this.iData =  new FormData();
    
  //   this.iData.append('image', this.image_upload, this.image_upload.name);
  //   console.log(this.iData)
  //   this.http.put('http://' + this.dataservice.domain_name + '/scrum/api/scrumgoals/', this.iData,
  //     this.dataservice.authOptions).subscribe(
  //       data => {
  //         this.dataservice.users = data['data'];
  //         this.dataservice.message = data['message'];
  //         this.filterSprint(this.dataservice.sprints)
  //       },
  //       err => {
  //         console.error(err);
  //         if(err['status'] == 401)
  //          {
  //           this.dataservice.message = 'Session Invalid or Expired. Please Login.';
  //           this.dataservice.logout();
  //          } else
  //          {
  //             this.dataservice.message = 'Unexpected Error!';    
  //           }
  //         }
  //       );
  // }

  addGoal()
  {
    console.log("inside addgoal" + this.on_user);


    this.dataservice.addGoal(this.on_user);
  }
  
  setSelectedUser(id)
  {
    this.id_hover = id;    
  }
  
  logout()
  {
    this.dataservice.message = 'Thank you for using Scrum!';
    this.websocket.close();
    this.dataservice.logout();
  }
  
  ngOnDestroy()
  {
    this.subs.unsubscribe();  
    this.dragula.destroy('mainTable');
  }

  scrollIntoView(anchorHash) {
    this.id_click = parseInt(anchorHash.substring(1), 10);
    setTimeout(() => {
        const anchor = document.getElementById(anchorHash);
        console.log(anchorHash);
        if (anchor) {
            anchor.focus();
            anchor.scrollIntoView();
        }
    });
}

//   addGoalModal(){
//     $(document).ready(function(){
//         // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
//         $('.modal-trigger').leanModal();
//       });
//   }


  selectFile(event) {
    console.log(event)
    this.image_upload =event.target.files;
  }

  imageUpload() {
    if (this.image_upload == null) {
      this.dataservice.message = "No file selected!!!"
      console.log("No file selected!");
      return
    }
    let details = {
        'mode': 1,
        'goal_id': this.goal_id, 
        'project_id': this.dataservice.project,
        
      };
    let file: File = this.image_upload[0];
    console.log(this.dataservice.imageAuthOptions)
    console.log(file)

    this.iData =  new FormData();
    
    this.iData.append('image', file, file.name);
    this.iData.append('mode', 1);
    this.iData.append('goal_id', this.goal_id);
    this.iData.append('project_id', this.dataservice.project);
    console.log(file)
    console.log(this.iData)
    this.http.put('http://' + this.dataservice.domain_name + '/scrum/api/scrumgoals/', this.iData,
      this.dataservice.imageAuthOptions)
      .subscribe(
        data => {
          this.dataservice.users = data['data'];
          this.dataservice.message = data['message'];
          this.filterSprint(this.dataservice.sprints)
        },
        err => {
          console.error(err);
          if(err['status'] == 401)
           {
            this.dataservice.message = 'Session Invalid or Expired. Please Login.';
            this.dataservice.logout();
           } else
           {
              this.dataservice.message = 'Unexpected Error!';    
            }
          }
        );
  }

  ResizeImage(iName) {
    console.log(iName)
    this.scrum_image = iName
  }

    CheckHistory(task) {
      console.log(task)
      this.task_history = task
      this.show_history = !this.show_history; 
  }


}
