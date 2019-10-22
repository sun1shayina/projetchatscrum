import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicVideosComponent } from './topic-labs.component';

describe('TopicVideosComponent', () => {
  let component: TopicVideosComponent;
  let fixture: ComponentFixture<TopicVideosComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopicVideosComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopicVideosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
