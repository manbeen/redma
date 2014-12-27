//
//  ViewController.m
//  REDMAApp
//
//  Created by Manbeen Kohli on 2014-12-26.
//  Copyright (c) 2014 Saj. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

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


- (IBAction)handleClick:(id)sender {
    [self getDataFromWebservice];
}

- (void) clearLabels {
    self.errorLabel.text = @"";
    self.temperatureLabel.text = @"";
    self.waterLabel.text = @"";
    self.smokeLabel.text = @"";
    self.timestampLabel.text = @"";
}

- (void) displayError {
    [self clearLabels];
    self.errorLabel.text = @"WebService connection failed :-(";
    self.errorLabel.textColor = [UIColor redColor];
}

-(void) getDataFromWebservice {
    bool errorOccurred = NO;
    @try {
        [self clearLabels];
        
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
                         } else {
                             valueAsString = [value stringValue];
                         }
                         
                         if([keyAsString isEqualToString:@"sensor1" ] ) {
                             self.temperatureLabel.text = valueAsString;
                             self.temperatureLabel.textColor = [UIColor greenColor];
                         } else if( [keyAsString isEqualToString:@"sensor2"]) {
                             self.smokeLabel.text = valueAsString;
                             self.smokeLabel.textColor = [UIColor greenColor];
                         } else if( [keyAsString isEqualToString:@"sensor3"]) {
                             self.waterLabel.text = valueAsString;
                             self.waterLabel.textColor = [UIColor greenColor];
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
