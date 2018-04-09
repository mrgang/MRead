//
//  ContentViewController.swift
//  ReadingNow
//
//  Created by iOS Developer on 2017/6/19.
//  Copyright © 2017年 lig. All rights reserved.
//

import UIKit

class ContentViewController: UIViewController, UITextViewDelegate, UIScrollViewDelegate {
    
    @IBOutlet weak var scrollView: UIScrollView!
    var uperDisplayView: UITextView!
    var mainDisplayView: UITextView!
    var nextDisplayView: UITextView!
    var book: BookCellContent!
    var uperContentURL: String?
    var contentURL = ""
    var nextContentURL: String?
    var fontSize: CGFloat = UserDefaults.standard.value(forKey: "FontSize") as? CGFloat ?? 22 {
        didSet {
            if fontSize < 15 {fontSize = 15}
            fontFamily = UIFont.boldSystemFont(ofSize: fontSize)
            UserDefaults.standard.set(fontSize, forKey: "FontSize")
            UserDefaults.standard.synchronize()
        }
    }
    var fontFamily = UIFont.boldSystemFont(ofSize: 22) {
        didSet{
            let paraph = NSMutableParagraphStyle()
            paraph.lineSpacing = 8
            mainDisplayView.attributedText = NSAttributedString(string: mainDisplayView.attributedText.string, attributes: [NSAttributedStringKey.font : fontFamily,NSAttributedStringKey.foregroundColor:#colorLiteral(red: 0.2821000648, green: 0.2821000648, blue: 0.2821000648, alpha: 1),NSAttributedStringKey.paragraphStyle: paraph,NSAttributedStringKey(rawValue: NSAttributedString.DocumentAttributeKey.documentType.rawValue): NSAttributedString.DocumentType.html])
        }
    }
    let settingView = UIView()
    let stackView: UIStackView = {
        let closeBtn = UIButton()
        let fontDBtn = UIButton()
        let fontABtn = UIButton()
        closeBtn.setTitle("关闭", for: .normal)
        fontDBtn.setTitle("A-", for: .normal)
        fontABtn.setTitle("A+", for: .normal)
        closeBtn.setTitleColor(.white, for: .normal)
        fontDBtn.setTitleColor(#colorLiteral(red: 0.2392156869, green: 0.6745098233, blue: 0.9686274529, alpha: 1), for: .normal)
        fontABtn.setTitleColor(#colorLiteral(red: 0.2392156869, green: 0.6745098233, blue: 0.9686274529, alpha: 1), for: .normal)
        
        closeBtn.setTitleColor(.black, for: .highlighted)
        fontDBtn.setTitleColor(.red, for: .highlighted)
        fontABtn.setTitleColor(.red, for: .highlighted)
        
        closeBtn.titleLabel?.font =  UIFont.boldSystemFont(ofSize: 18)
        fontDBtn.titleLabel?.font =  UIFont.boldSystemFont(ofSize: 20)
        fontABtn.titleLabel?.font =  UIFont.boldSystemFont(ofSize: 25)
        
        closeBtn.addTarget(self, action: #selector(closeSetting), for: .touchUpInside)
        fontDBtn.addTarget(self, action: #selector(fontSizeDecrise), for: .touchUpInside)
        fontABtn.addTarget(self, action: #selector(fontSizePlus), for: .touchUpInside)
        
        let stackView = UIStackView(arrangedSubviews: [closeBtn,fontDBtn,fontABtn])
        stackView.alignment = .fill
        stackView.distribution = .fillEqually
        stackView.axis = .horizontal
        stackView.spacing = 10
        var colorBtn1 = UIButton();colorBtn1.backgroundColor = #colorLiteral(red: 0.9603565335, green: 0.9405425191, blue: 0.8997241855, alpha: 1)
        colorBtn1.frame.size = CGSize(width: 20, height: 20)
        colorBtn1.layer.cornerRadius = 12
        var colorBtn2 = UIButton();colorBtn2.backgroundColor = #colorLiteral(red: 0.9560309052, green: 0.9154954553, blue: 0.7806045413, alpha: 1)
        colorBtn2.frame.size = CGSize(width: 20, height: 20)
        colorBtn2.layer.cornerRadius = 12
        var colorBtn3 = UIButton();colorBtn3.backgroundColor = #colorLiteral(red: 0.878980875, green: 0.9244450927, blue: 0.8759120107, alpha: 1)
        colorBtn3.frame.size = CGSize(width: 20, height: 20)
        colorBtn3.layer.cornerRadius = 12
        var colorBtn4 = UIButton();colorBtn4.backgroundColor = #colorLiteral(red: 0.8830786347, green: 0.9335067868, blue: 0.9497951865, alpha: 1)
        colorBtn4.frame.size = CGSize(width: 20, height: 20)
        colorBtn4.layer.cornerRadius = 12
        var colorBtn5 = UIButton();colorBtn5.backgroundColor = #colorLiteral(red: 0.9597762227, green: 0.8944482803, blue: 0.8938558102, alpha: 1)
        colorBtn5.frame.size = CGSize(width: 20, height: 20)
        colorBtn5.layer.cornerRadius = 12
        var colorBtn6 = UIButton();colorBtn6.backgroundColor = #colorLiteral(red: 0.8548294902, green: 0.8549499512, blue: 0.854791522, alpha: 1)
        colorBtn6.frame.size = CGSize(width: 20, height: 20)
        colorBtn6.layer.cornerRadius = 12
        
        colorBtn1.addTarget(self, action: #selector(getBackgroundColor(_:)), for: .touchUpInside)
        colorBtn2.addTarget(self, action: #selector(getBackgroundColor(_:)), for: .touchUpInside)
        colorBtn3.addTarget(self, action: #selector(getBackgroundColor(_:)), for: .touchUpInside)
        colorBtn4.addTarget(self, action: #selector(getBackgroundColor(_:)), for: .touchUpInside)
        colorBtn5.addTarget(self, action: #selector(getBackgroundColor(_:)), for: .touchUpInside)
        colorBtn6.addTarget(self, action: #selector(getBackgroundColor(_:)), for: .touchUpInside)
        
        let colorStackView = UIStackView(arrangedSubviews: [
            UIView(frame: CGRect(x: 0, y: 0, width: 20, height: 20)),
            colorBtn1,colorBtn2,colorBtn3,
            colorBtn4, colorBtn5,colorBtn6,
            UIView(frame: CGRect(x: 0, y: 0, width: 20, height: 20))])
        colorStackView.alignment = .fill
        colorStackView.distribution = .equalSpacing
        colorStackView.axis = .horizontal
        colorStackView.spacing = 10
        
        let outerView = UIStackView(arrangedSubviews: [stackView, colorStackView])
        outerView.alignment = .fill
        outerView.distribution = .fillEqually
        outerView.axis = .vertical
        outerView.spacing = 5
        return outerView
    }()
    @objc func getBackgroundColor(_ sender: UIButton) {
        if let bg = sender.backgroundColor {
            uperDisplayView.backgroundColor = bg
            mainDisplayView.backgroundColor = bg
            nextDisplayView.backgroundColor = bg
            UserDefaults.standard.setValue(NSKeyedArchiver.archivedData(withRootObject: bg), forKey: "ContentBG")
            UserDefaults.standard.synchronize()
        }
    }
    
    @objc func closeSetting(){
        settingView.isHidden = true
    }
    @objc func fontSizeDecrise(){
        fontSize -= 1
    }
    @objc func fontSizePlus(){
        fontSize += 1
    }
    
    func initSettingView() {
        view.addSubview(settingView)
        view.bringSubview(toFront: settingView)
        settingView.addSubview(stackView)
        stackView.translatesAutoresizingMaskIntoConstraints = false
        settingView.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            settingView.leftAnchor.constraint(equalTo: view.leftAnchor),
            settingView.rightAnchor.constraint(equalTo: view.rightAnchor),
            settingView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            settingView.heightAnchor.constraint(equalToConstant: 70),
            stackView.leftAnchor.constraint(equalTo: settingView.leftAnchor),
            stackView.rightAnchor.constraint(equalTo: settingView.rightAnchor),
            stackView.topAnchor.constraint(equalTo: settingView.topAnchor),
            stackView.bottomAnchor.constraint(equalTo: settingView.bottomAnchor)
            ])
        settingView.backgroundColor = UIColor(white: 0, alpha: 0.7)
        settingView.isHidden = true
    }
    
    @IBAction func settingFont(_ sender: Any) {
        settingView.isHidden = !settingView.isHidden
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        title = "加载中..."
        let mWidth = scrollView.frame.width
        let mHeight = scrollView.frame.height
        uperDisplayView = UITextView(frame: CGRect(x: 0, y: 0, width: mWidth, height: mHeight))
        mainDisplayView = UITextView(frame: CGRect(x: mWidth, y: 0, width: mWidth, height: mHeight))
        nextDisplayView = UITextView(frame: CGRect(x: mWidth*2, y: 0, width: mWidth, height: mHeight))
        scrollView.addSubview(uperDisplayView)
        scrollView.addSubview(mainDisplayView)
        scrollView.addSubview(nextDisplayView)
        scrollView.contentSize = CGSize(width: mWidth * 3, height: mHeight)
        
        uperDisplayView.isEditable = false
        mainDisplayView.isEditable = false
        nextDisplayView.isEditable = false
        uperDisplayView.isSelectable = false
        mainDisplayView.isSelectable = false
        nextDisplayView.isSelectable = false
        
        uperDisplayView.delegate = self
        mainDisplayView.delegate = self
        nextDisplayView.delegate = self
        scrollView.delegate = self
        if let colorData = UserDefaults.standard.value(forKey: "ContentBG"), let bg = NSKeyedUnarchiver.unarchiveObject(with: colorData as! Data) as? UIColor {
            uperDisplayView.backgroundColor = bg
            mainDisplayView.backgroundColor = bg
            nextDisplayView.backgroundColor = bg
        }else {
            uperDisplayView.backgroundColor = #colorLiteral(red: 0.9603565335, green: 0.9405425191, blue: 0.8997241855, alpha: 1)
            mainDisplayView.backgroundColor = #colorLiteral(red: 0.9603565335, green: 0.9405425191, blue: 0.8997241855, alpha: 1)
            nextDisplayView.backgroundColor = #colorLiteral(red: 0.9603565335, green: 0.9405425191, blue: 0.8997241855, alpha: 1)
        }
        navigationController?.navigationBar.prefersLargeTitles = false
        contentURL = book.url
        scrollView.contentOffset.x = scrollView.frame.width
        loadMainContent()
        initSettingView()
    }
    
    func nextChapter() {
        if let nc = nextContentURL {
            contentURL = nc
            mainDisplayView.attributedText = NSAttributedString(string: "\n\n\n\n加载中...")
            title = "加载中..."
            loadMainContent()
        }else{
            mainDisplayView.attributedText = NSAttributedString(string: "\n\n\n\n已经看到最新章节了！")
            title = "没有了..."
        }
    }
    func uperChapter() {
        if let nc = uperContentURL {
            contentURL = nc
            mainDisplayView.attributedText = NSAttributedString(string: "\n\n\n\n加载中...")
            title = "加载中..."
            loadMainContent()
        }else{
            mainDisplayView.attributedText = NSAttributedString(string: "\n\n\n\n已经到第一章了！")
            title = "没有了..."
        }
    }
    
    func loadMainContent(){
        let paraph = NSMutableParagraphStyle()
        paraph.lineSpacing = 8
        URLSession.shared.dataTask(with: URL(string: "http://hsmart.xzzjw.cn/Books/Analyzer/contentPage?path="+contentURL)!) {[weak self] (data, resp, error) in
            DispatchQueue.main.async {
                if let data = data, let result = try? JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String:Any]  {
                    let success = result["success"] as! Bool
                    if success {
                        let content = result["data"] as! [String:String]
                        self?.mainDisplayView.attributedText = NSAttributedString(string: "\n\(content["content"]!)", attributes: [NSAttributedStringKey.font : UIFont.boldSystemFont(ofSize: self?.fontSize ?? 22),NSAttributedStringKey.foregroundColor:#colorLiteral(red: 0.2821000648, green: 0.2821000648, blue: 0.2821000648, alpha: 1),NSAttributedStringKey.paragraphStyle: paraph,NSAttributedStringKey(rawValue: NSAttributedString.DocumentAttributeKey.documentType.rawValue): NSAttributedString.DocumentType.html])
                        let nextURL = content["nextChap"]!
                        let uperURL = content["preChap"]!
                        self?.title = content["title"]
                        if nextURL.hasSuffix(".html"){
                            self?.nextContentURL = nextURL
                            UserDefaults.standard.set(nextURL, forKey: content["title"]!)
                            UserDefaults.standard.synchronize()
                        }else {
                            self?.nextContentURL = nil
                        }
                        if uperURL.hasSuffix(".html"){
                            self?.uperContentURL = uperURL
                        }else {
                            self?.uperContentURL = nil
                        }
                    }
                    
                }else {
                    let alert = UIAlertController(title: "提示", message: error?.localizedDescription, preferredStyle: .alert)
                    alert.addAction(UIAlertAction(title: "确定", style: .default))
                    self?.present(alert, animated: true)
                    
                }
            }
            }.resume()
    }
    var _lastPosition: CGFloat = 0
    var isHiddeStatusBar = false {
        didSet{
            setNeedsStatusBarAppearanceUpdate()
        }
    }
    override func viewWillDisappear(_ animated: Bool) {
        self.navigationController?.navigationBar.isHidden = false
    }
    override var prefersStatusBarHidden: Bool { return isHiddeStatusBar  }
    func scrollViewDidScroll(_ scrollView: UIScrollView) {
        let currentPostion = scrollView.contentOffset.y
        if abs(currentPostion) < 125 {
            self.navigationController?.navigationBar.isHidden = false
            return
        }
        if currentPostion - _lastPosition > 50 {//ScrollUp
            _lastPosition = currentPostion
            if let nav = navigationController, !nav.navigationBar.isHidden {
                UIView.animate(withDuration: 0.2){
                    //self.isHiddeStatusBar = true
                    self.navigationController?.navigationBar.isHidden = true
                }
            }
        }else if _lastPosition - currentPostion > 50{//ScrollDown
            _lastPosition = currentPostion
            if let nav = navigationController, nav.navigationBar.isHidden {
                UIView.animate(withDuration: 0.2){
                    //self.isHiddeStatusBar = false
                    self.navigationController?.navigationBar.isHidden = false
                }
            }
        }
    }
    var startScrollX: CGFloat?
    func scrollViewWillBeginDecelerating(_ scrollView: UIScrollView) {
        startScrollX = scrollView.contentOffset.x
    }
    
    func scrollViewDidEndDecelerating(_ scrollView: UIScrollView) {
        if startScrollX == scrollView.contentOffset.x {return}
        if scrollView.contentOffset.x == scrollView.frame.width*2 {
            (mainDisplayView.frame, uperDisplayView.frame) = (uperDisplayView.frame, mainDisplayView.frame)
            (uperDisplayView.frame, nextDisplayView.frame) = (nextDisplayView.frame, uperDisplayView.frame)
            scrollView.contentOffset.x = scrollView.frame.width
            (mainDisplayView, nextDisplayView) = (nextDisplayView, mainDisplayView)
            (uperDisplayView, nextDisplayView) = (nextDisplayView, uperDisplayView)
            nextDisplayView.attributedText = NSAttributedString(string: "\n\n\n\n\n加载中...")
            uperDisplayView.attributedText = NSAttributedString(string: "\n\n\n\n\n加载中...")
            nextChapter()
        }else if scrollView.contentOffset.x == 0 {
            (mainDisplayView.frame, nextDisplayView.frame) = (nextDisplayView.frame, mainDisplayView.frame)
            (uperDisplayView.frame, nextDisplayView.frame) = (nextDisplayView.frame, uperDisplayView.frame)
            scrollView.contentOffset.x = scrollView.frame.width
            (mainDisplayView, uperDisplayView) = (uperDisplayView, mainDisplayView)
            (uperDisplayView, nextDisplayView) = (nextDisplayView, uperDisplayView)
            nextDisplayView.attributedText = NSAttributedString(string: "\n\n\n\n\n加载中...")
            uperDisplayView.attributedText = NSAttributedString(string: "\n\n\n\n\n加载中...")
            uperChapter()
        }
    }
    
}
