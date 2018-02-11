//
//  LastTenTableViewController.swift
//  ReadingNow
//
//  Created by iOS Developer on 2017/6/19.
//  Copyright © 2017年 lig. All rights reserved.
//

import UIKit
class LastTenTableViewController: UITableViewController {
    var tenChapters = [(String,String)]()
    var allChapters = ""
    var shouldBeRed: Int?
    var book: BookCellContent!
    
    override func viewDidLoad() {
        navigationController?.navigationBar.prefersLargeTitles = false
        tenChapters = book.latestedTen
        tableView.reloadData()
    }
    
    @IBAction func LoadAllChapters(_ sender: UIBarButtonItem) {
        title = "加载中..."
        URLSession.shared.dataTask(with: URL(string: "http://hsmart.xzzjw.cn/Book/Analyzer?actionType=3&distination="+book.all)!) {[weak self] (data, resp, error) in
            if let data = data , let result = try? JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String:Any]{
                let success = result["success"] as! Bool
                if success {
                    let content = result["data"] as! [String:Any]
                    let _tenChapters = (content["chapters"] as! [[String:String]]).map({ item -> (String,String) in
                        return (item["name"]!,item["path"]!)
                    })
                    
                    let chapterName = content["title"] as! String
                    
                    DispatchQueue.main.async {
                        self?.tenChapters = _tenChapters
                        self?.tableView.reloadData()
                        self?.title = chapterName
                        var latestIndex: Int?
                        if let latestedRead = UserDefaults.standard.value(forKey: chapterName) as? String{
                            for (index,value) in _tenChapters.enumerated() {
                                if value.1.contains(latestedRead) {
                                    latestIndex = index
                                    break
                                }
                            }
                        }
                        if let latestIndex = latestIndex {
                            let indexPath = IndexPath(row: latestIndex, section: 0)
                            self?.tableView.scrollToRow(at: indexPath, at: .top, animated: true)
                            self?.shouldBeRed = latestIndex
                            self?.tableView.reloadRows(at: [indexPath], with: .automatic)
                        }
                    }
                }
            }else {
                DispatchQueue.main.async {
                    let alert = UIAlertController(title: "提示", message: error?.localizedDescription, preferredStyle: .alert)
                    alert.addAction(UIAlertAction(title: "确定", style: .default))
                    self?.present(alert, animated: true)
                }
            }
            
        }.resume()
    }
    
    
    // MARK: - Table view data source
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return tenChapters.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "title cell", for: indexPath)
        cell.textLabel?.text = tenChapters[indexPath.row].0
        if shouldBeRed == indexPath.row {
            cell.textLabel?.textColor = .red
        }else {
            cell.textLabel?.textColor = .black
        }
        return cell
    }
    
    // MARK: - Navigation
    
    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "showContent", let dest = segue.destination as? ContentViewController {
            let indexPath = tableView.indexPathForSelectedRow!
            dest.book = book
            dest.book.url = tenChapters[indexPath.row].1
        }
    }
}
