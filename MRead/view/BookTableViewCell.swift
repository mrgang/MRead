//
//  BookTableViewCell.swift
//  MRead
//
//  Created by 李刚 on 2017/9/24.
//  Copyright © 2017年 李刚. All rights reserved.
//

import UIKit

class BookTableViewCell: UITableViewCell {

    @IBOutlet weak var bookCover: UIImageView!
    
    @IBOutlet weak var bookName: UILabel!
    
    @IBOutlet weak var updateTime: UILabel!
    
    @IBOutlet weak var latestedChapter: UIButton!
    
    @IBOutlet weak var origin: UILabel!
    
    @IBAction func showLatestedChapter(_ sender: Any) {
        showLatestedChapterDelegate?.getLastChapterURL(cell: self)
    }
    weak var showLatestedChapterDelegate: GetLastChapterURLDelegate?
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
}
