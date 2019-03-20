//
//  BookTableViewController.swift
//  MRead
//
//  Created by 李刚 on 2017/9/24.
//  Copyright © 2017年 李刚. All rights reserved.
//

import UIKit
import Kingfisher
import MJRefresh
class BookTableViewController: UITableViewController, GetLastChapterURLDelegate,UISearchBarDelegate,UISearchControllerDelegate{
    var bookURLs = [String]()
    var BookCellContentCache = [Int:BookCellContent]()
    var task: URLSessionTask?
    var tasks = [URLSessionTask]()
    var isSearching = false
    let sc = UISearchController(searchResultsController: nil)
    override func viewDidLoad() {
        super.viewDidLoad()
        navigationController?.navigationBar.barStyle = .blackTranslucent
        navigationController?.navigationBar.barTintColor = #colorLiteral(red: 0.2392156869, green: 0.6745098233, blue: 0.9686274529, alpha: 1)
        navigationController?.navigationBar.tintColor = .white
        tableView.register(UINib(nibName: "BookTableViewCell", bundle: nil), forCellReuseIdentifier: "bookcell")
        //滑动时隐藏searchBar
        navigationItem.hidesSearchBarWhenScrolling = true
        //将searchController赋值给navigationItem
        navigationItem.searchController = sc
        sc.searchBar.placeholder = "书名"
        sc.searchBar.showsCancelButton = false
        sc.searchBar.delegate = self
        sc.searchBar.setValue("取消", forKey: "_cancelButtonText")
        sc.delegate = self
        tableView.mj_header = MJRefreshNormalHeader(refreshingBlock: {
            [unowned self] in
            for t in self.tasks {
                t.cancel()
            }
            self.tasks.removeAll()
            self.getMyBookList()
        })
        tableView.mj_header.beginRefreshing()
    }
    override func viewWillAppear(_ animated: Bool) {
        //设置大字体
        navigationController?.navigationBar.prefersLargeTitles = false
    }
    override func viewWillDisappear(_ animated: Bool) {
        //设置大字体
        navigationController?.navigationBar.prefersLargeTitles = false
    }
    
    func searchBarSearchButtonClicked(_ searchBar: UISearchBar) {
        if let searchText = searchBar.text,!searchText.isEmpty {
            //startSearch
            searchBooks(searchContent: searchText)
        }
    }
    func willDismissSearchController(_ searchController: UISearchController) {
        //isSearching = false
        //BookCellContentCache.removeAll()
        //getMyBookList()
    }
    func willPresentSearchController(_ searchController: UISearchController) {
        isSearching = true
        bookURLs.removeAll()
        BookCellContentCache.removeAll()
        tableView.reloadData()
    }
    func searchBooks(searchContent: String){
        for t in tasks {
            t.cancel()
        }
        tasks.removeAll()
        bookURLs.removeAll()
        BookCellContentCache.removeAll()
        tableView.reloadData()
        let session = URLSession.shared
        task?.cancel()
        task = session.dataTask(with: URL(string: SERVERPATH+"/Search/\(searchContent.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)!)")!){[weak self] (data, resp, error) in
            DispatchQueue.main.async {
                if let data = data, let books = try? JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [[String: String]] {
                    let results = books.map({ item -> String in
                        return item["url"]!
                    })
                    self?.bookURLs = results
                    self?.tableView.reloadData()
                }
            }
        }
        task?.resume()
    }
    var flag = true
    
    @IBAction func getDefaultBooks() {
        for t in tasks {
            t.cancel()
        }
        tasks.removeAll()
        let session = URLSession.shared
        let _task = session.dataTask(with: URL(string: "https://raw.githubusercontent.com/mrgang/mrgang.github.io/master/mystory.json")!) {[weak weakSelf = self] (data, resp, error) in
            DispatchQueue.main.async {
                if let data = data, let books = try? JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [Any]{
                    let URLs: [String] = books.map({ (item) -> String in
                        (item as! [String:String])["url"]!
                    })
                    let paths = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true) as NSArray
                    let documentDirectory = paths[0] as! String
                    let path = documentDirectory.appending("/urls.plist")
                    (URLs as NSArray).write(toFile: path, atomically: false)
                    weakSelf?.getMyBookList()
                }else {
                    let alert = UIAlertController(title: "提示", message: error?.localizedDescription, preferredStyle: .alert)
                    alert.addAction(UIAlertAction(title: "确定", style: .default))
                    weakSelf?.present(alert, animated: true)
                }
            }
        }
        _task.resume()
        tasks.append(_task)
    }
    func getMyBookList(){
        isSearching = false
        let paths = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true) as NSArray
        let documentDirectory = paths[0] as! String
        let path = documentDirectory.appending("/urls.plist")
        let fileManager = FileManager.default
        if(!fileManager.fileExists(atPath: path)){
            let defaultPath = Bundle.main.path(forResource: "defaultURL", ofType: "plist")!
            do{
                try fileManager.copyItem(atPath: defaultPath, toPath: path)
            }catch{
                print("copy failure.")
            }
        }
        
        if let array = NSArray(contentsOfFile: path) as? [String]{
            bookURLs = array
            BookCellContentCache.removeAll()
            tableView.reloadData()
        }
        tableView.mj_header.endRefreshing()
    }
    func getLastChapterURL(cell: BookTableViewCell) {
        if let indexPath = tableView.indexPath(for: cell),let book = BookCellContentCache[indexPath.row] {
            performSegue(withIdentifier: "showContent", sender: book)
        }
    }
    
    // MARK: - Table view data source
    override func numberOfSections(in tableView: UITableView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        if bookURLs.count == 0 {
            tableView.separatorStyle = .none
            let bg = UILabel()
            let paraph = NSMutableParagraphStyle()
            paraph.lineSpacing = 8
            bg.attributedText = NSAttributedString(string: "\n\n\n空空的", attributes: [NSAttributedString.Key.font: UIFont.boldSystemFont(ofSize: 18),NSAttributedString.Key.paragraphStyle:paraph,NSAttributedString.Key.foregroundColor: #colorLiteral(red: 0.501960814, green: 0.501960814, blue: 0.501960814, alpha: 1)])
            bg.numberOfLines = 0
            bg.textAlignment = .center
            tableView.backgroundView = bg
        }else {
            tableView.separatorStyle = .singleLine
            tableView.backgroundView = nil
        }
        return 1
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return bookURLs.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "bookcell", for: indexPath) as! BookTableViewCell
        cell.bookName.text = "";
        cell.updateTime.text = "";
        cell.latestedChapter.setTitle("", for: .normal)
        cell.latestedChapter.isUserInteractionEnabled = false
        cell.origin.text = ""
        cell.isUserInteractionEnabled = false
        let index = indexPath.row
        //chech weather has local cache
        if let cellCache = BookCellContentCache[index] {
            cell.bookName.text = cellCache.name + "\t" + cellCache.author
            cell.updateTime.text = cellCache.time
            cell.latestedChapter.setTitle(cellCache.chapter, for: .normal)
            cell.bookCover.kf.setImage(with: URL(string: cellCache.img))
            cell.latestedChapter.isUserInteractionEnabled = true
            cell.isUserInteractionEnabled = true
            cell.origin.text = cellCache.host
        }else {
            //load data from net
            let session = URLSession.shared
            let path_str = SERVERPATH+"/Analyzer/mainPage?path="+bookURLs[indexPath.row]
            let _task = session.dataTask(with: URL(string: path_str)!){[weak weakSelf = self] (data, resp, error) in
                DispatchQueue.main.async {
                    if let data = data, let result = try? JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String: Any] {
                        let success = result["success"] as! Bool
                        if success {
                            let info = result["data"] as! [String:Any]
                            let host = info["host"] as! String
                            let _name = info["name"] as! String
                            let _author = info["author"] as! String
                            let _time = info["uptime"] as! String
                            let _chapter = info["latestName"] as? String ?? ""
                            let _url = info["latestPath"] as! String
                            let _img = info["image"] as! String
                            let _all = info["allChapter"] as! String
                            
                            cell.bookName.text = _name + "\t" + _author
                            cell.updateTime.text = _time.trimmingCharacters(in: CharacterSet.whitespacesAndNewlines)
                            cell.latestedChapter.setTitle( _chapter, for: .normal)
                            cell.bookCover.kf.setImage(with: URL(string: _img))
                            cell.latestedChapter.isUserInteractionEnabled = true
                            cell.isUserInteractionEnabled = true
                            cell.origin.text = host
                            var latestedTen = [(String,String)]()
                            for chapter in (info["lastTen"] as! [[String:String]]) {
                                latestedTen.append((chapter["name"]!,chapter["path"]!))
                            }
                            weakSelf?.BookCellContentCache[index] = BookCellContent(name: _name, author: _author, time: cell.updateTime.text!, chapter: _chapter, url: _url, img: _img, all: _all.replacingOccurrences(of: " ", with: ""), latestedTen: latestedTen, host: host)
                            weakSelf?.tableView.reloadRows(at: [IndexPath.init(row: index, section: 0)], with: UITableView.RowAnimation.fade)
                        }
                    }else {
                        if let e = error, e.localizedDescription.contains("cancelled") {
                            return
                        }
                        let alert = UIAlertController(title: "提示", message: error?.localizedDescription, preferredStyle: .alert)
                        alert.addAction(UIAlertAction(title: "确定", style: .default))
                        if self.isSearching {
                            weakSelf?.sc.present(alert, animated: true)
                        }else{
                            weakSelf?.present(alert, animated: true)
                        }
                    }
                }
            }
            _task.resume()
            tasks.append(_task)
        }
        cell.showLatestedChapterDelegate = self
        return cell
    }
    
    override func tableView(_ tableView: UITableView, editActionsForRowAt indexPath: IndexPath) -> [UITableViewRowAction]? {
        if isSearching {
            let action = UITableViewRowAction(style: .default, title: "添加到书单") { (act, indexPath) in
                if !self.bookURLs[indexPath.row].isEmpty {
                    let paths = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true) as NSArray
                    let documentDirectory = paths[0] as! String
                    let path = documentDirectory.appending("/urls.plist")
                    if var array = NSArray(contentsOfFile: path) as? [String]{
                        array.append(self.bookURLs[indexPath.row])
                        (array as NSArray).write(toFile: path, atomically: false)
                        let alert = UIAlertController(title: "提示", message: "添加成功", preferredStyle: .alert)
                        self.sc.present(alert, animated: true){
                            alert.dismiss(animated: true)
                        }
                        tableView.isEditing = false
                    }
                }else{
                    let alert = UIAlertController(title: "提示", message: "无法添加", preferredStyle: .alert)
                    self.sc.present(alert, animated: true){
                        alert.dismiss(animated: true)
                    }
                }
            }
            action.backgroundColor = .darkGray
            return [action]
        }
        let action = UITableViewRowAction(style: .destructive, title: "移除") { (act, indexPath) in
            self.bookURLs.remove(at: indexPath.row)
            //tableView.deleteRows(at: [indexPath], with: .fade)
            //self.BookCellContentCache[indexPath.row] = nil
            self.BookCellContentCache.removeAll()
            let paths = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true) as NSArray
            let documentDirectory = paths[0] as! String
            let path = documentDirectory.appending("/urls.plist")
            (self.bookURLs as NSArray).write(toFile: path, atomically: false)
            self.tableView.reloadData()
        }
        return [action]
    }
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        performSegue(withIdentifier: "showChapters", sender: indexPath.row)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "showContent" {
            let dest = segue.destination as! ContentViewController
            dest.book = sender as? BookCellContent
        }else if segue.identifier == "showChapters" {
            let dest = segue.destination as! LastTenTableViewController
            dest.book = BookCellContentCache[sender as! Int]!
        }
    }
}
protocol GetLastChapterURLDelegate: class {
    func getLastChapterURL(cell: BookTableViewCell)
}
