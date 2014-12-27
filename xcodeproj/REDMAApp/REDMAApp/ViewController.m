//
//  ViewController.m
//  REDMAApp
//
//  Created by Manbeen Kohli on 2014-12-26.
//  Copyright (c) 2014 Saj. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()
{
    NSString *waterValue;
    NSString *smokeValue;
    bool waterButtonToggle;
    bool smokeButtonToggle;
    bool waterOK;
    bool smokeOK;
}

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    [self getDataFromWebservice];
    
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)handleRefreshButtonClick:(id)sender {
    [self getDataFromWebservice];
}


- (IBAction)handleSmokeButtonClick:(id)sender {
    if(smokeButtonToggle) {
        [self.smokeButton setTitle:smokeValue forState:UIControlStateNormal];
        smokeButtonToggle = NO;
    } else {
        if(smokeOK) {
            [self.smokeButton setTitle:@"OK" forState:UIControlStateNormal];
        } else {
            [self.smokeButton setTitle:@"Alert" forState:UIControlStateNormal];
        }
        smokeButtonToggle = YES;
    }
}

- (IBAction)handleWaterButtonClick:(id)sender {
    if(waterButtonToggle) {
        [self.waterButton setTitle:waterValue forState:UIControlStateNormal];
        waterButtonToggle = NO;
    } else {
        if(waterOK) {
            [self.waterButton setTitle:@"OK" forState:UIControlStateNormal];
        } else {
            [self.waterButton setTitle:@"Alert" forState:UIControlStateNormal];
        }
        waterButtonToggle = YES;
    }
}

- (void) clearData{
    waterValue = @"";
    smokeValue = @"";
    waterButtonToggle = YES;
    smokeButtonToggle = YES;
    waterOK = YES;
    smokeOK = YES;
    self.errorLabel.text = @"";
    self.temperatureLabel.text = @"";
    [self.waterButton setTitle:@"" forState:UIControlStateNormal];
    [self.smokeButton setTitle:@"" forState:UIControlStateNormal];
    self.timestampLabel.text = @"";
}

- (void) displayError {
    [self clearData];
    self.errorLabel.text = @"WebService connection failed :-(";
    self.errorLabel.textColor = [UIColor redColor];
}

-(void) getDataFromWebservice {
    bool errorOccurred = NO;
    @try {
        [self clearData];
        
        NSURL *subscriberURL = [NSURL URLWithString: @"http://192.168.1.102:3000/sensoryData/1"];
        NSURLRequest *subscriberRequest = [NSURLRequest requestWithURL:subscriberURL];
        
        [NSURLConnection sendAsynchronousRequest:subscriberRequest
                                           queue:[NSOperationQueue mainQueue]
                               completionHandler:^(NSURLResponse *response,
                                                   NSData *data, NSError *connectionError)
         {
             if (data.length > 0 && connectionError == nil) {
                 NSError *myError = nil;
                 NSDictionary *subscriberResDict = [NSJSONSerialization
                                                    JSONObjectWithData:data
                                                    options:0
                                                    error:&myError];
                 NSArray *subscriberJSONRes = [subscriberResDict objectForKey:@"json"];
                 for (id tempElem in subscriberJSONRes) {
                     if( ![tempElem isKindOfClass:[NSDictionary class]]) {
                         // this should never happen
                         NSLog(@"The value %@ in the array is not a dictionary", [tempElem stringValue]);
                         continue;
                     }
                     NSDictionary *elem = (NSDictionary*)tempElem;
                     for(id key in elem) {
                         id value = [elem objectForKey:key];
                         NSString *keyAsString = nil;
                         if([key isKindOfClass:[NSString class]]) {
                            keyAsString = (NSString *)key;
                         } else {
                             keyAsString = [key stringValue];
                         }
                         NSString *valueAsString = nil;
                         if([value isKindOfClass:[NSString class]]) {
                             valueAsString = (NSString *)value;
                         } else if ([value isKindOfClass:[NSNumber class]]) {
                             NSNumberFormatter *numberFormatter = [[NSNumberFormatter alloc] init];
                             [numberFormatter setNumberStyle:NSNumberFormatterDecimalStyle];
                             [numberFormatter setUsesGroupingSeparator:NO];
                             [numberFormatter setMaximumFractionDigits:2];
                             [numberFormatter setMinimumFractionDigits:0];
                             valueAsString = [numberFormatter stringFromNumber:(NSNumber*)value];
                         } else {
                             valueAsString = [value stringValue];
                         }
                         
                         if([keyAsString isEqualToString:@"sensor1" ] ) {
                             self.temperatureLabel.text = valueAsString;
                         } else if([keyAsString isEqualToString:@"sensor1th" ]) {
                             if ([value isKindOfClass:[NSNumber class]]) {
                                 float tempVal = [(NSNumber*)value floatValue];
                                 if(tempVal > 0.0) {
                                     // we have an issue
                                     self.temperatureLabel.textColor = [UIColor redColor];
                                 } else {
                                     // all is good
                                     self.temperatureLabel.textColor = [UIColor greenColor];
                                 }
                             } else {
                                 // this should never happen
                                 NSLog(@"sensorth1 is not a float value");
                             }
                         } else if( [keyAsString isEqualToString:@"sensor2"]) {
                             waterValue = valueAsString;
                         } else if([keyAsString isEqualToString:@"sensorth2" ]) {
                             if ([value isKindOfClass:[NSNumber class]]) {
                                 float tempVal = [(NSNumber*)value floatValue];
                                 if(tempVal > 0.0) {
                                     // we have an issue
                                     [self.waterButton setTitle:@"Alert" forState:UIControlStateNormal];
                                     [self.waterButton setTitleColor:[UIColor redColor] forState:UIControlStateNormal];
                                     waterOK = NO;
                                 } else {
                                     // all is good
                                     [self.waterButton setTitle:@"OK" forState:UIControlStateNormal];
                                     [self.waterButton setTitleColor:[UIColor greenColor] forState:UIControlStateNormal];
                                     waterOK = YES;
                                 }
                             } else {
                                 // this should never happen
                                 NSLog(@"sensorth2 is not a float value");
                             }
                         } else if( [keyAsString isEqualToString:@"sensor3"]) {
                             smokeValue = valueAsString;
                         } else if([keyAsString isEqualToString:@"sensorth3" ]) {
                             if ([value isKindOfClass:[NSNumber class]]) {
                                 float tempVal = [(NSNumber*)value floatValue];
                                 if(tempVal > 0.0) {
                                     // we have an issue
                                     [self.smokeButton setTitle:@"Alert" forState:UIControlStateNormal];
                                     [self.smokeButton setTitleColor:[UIColor redColor] forState:UIControlStateNormal];
                                     smokeOK = NO;
                                 } else {
                                     // all is good
                                     [self.smokeButton setTitle:@"OK" forState:UIControlStateNormal];
                                     [self.smokeButton setTitleColor:[UIColor greenColor] forState:UIControlStateNormal];
                                     smokeOK = YES;
                                 }
                             } else {
                                 // this should never happen
                                 NSLog(@"sensorth2 is not a float value");
                             }
                         } else if( [keyAsString isEqualToString:@"timestamp"]) {
                             self.timestampLabel.text = valueAsString;
                         }
                     }
                 }
             } else {
                 [self displayError];
             }
         }];

    }
    @catch (NSException *exception) {
        NSLog(exception.description);
        errorOccurred = YES;
    }
    @finally {
        if(errorOccurred == YES) {
            [self displayError];
        }
    }
}

@end
