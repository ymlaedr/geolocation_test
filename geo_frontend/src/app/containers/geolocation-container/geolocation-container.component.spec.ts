import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GeolocationContainerComponent } from './geolocation-container.component';

describe('GeolocationContainerComponent', () => {
  let component: GeolocationContainerComponent;
  let fixture: ComponentFixture<GeolocationContainerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GeolocationContainerComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GeolocationContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
