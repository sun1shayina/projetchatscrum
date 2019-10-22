import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupClassComponent } from './group-class.component';

describe('GroupClassComponent', () => {
  let component: GroupClassComponent;
  let fixture: ComponentFixture<GroupClassComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GroupClassComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GroupClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
