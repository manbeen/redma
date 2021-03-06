//
//  ViewController.h
//  REDMAApp
//
//  Created by Sajeev Kohli on 2014-12-26.
//  Copyright (c) 2014 Saj. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface ViewController : UIViewController

@property (strong, nonatomic) IBOutlet UILabel *errorLabel;
@property (strong, nonatomic) IBOutlet UILabel *temperatureLabel;
@property (strong, nonatomic) IBOutlet UILabel *timestampLabel;
@property (strong, nonatomic) IBOutlet UIButton *smokeButton;
@property (strong, nonatomic) IBOutlet UIButton *waterButton;

@end

