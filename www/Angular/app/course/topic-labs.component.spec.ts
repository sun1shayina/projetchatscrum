import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicLabsComponent } from './topic-labs.component';

describe('TopicLabsComponent', () => {
  let component: TopicLabsComponent;
  let fixture: ComponentFixture<TopicLabsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopicLabsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopicLabsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
